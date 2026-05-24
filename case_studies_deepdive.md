# Case Studies Deep-Dive: AAR-Discovered Methods for Weak-to-Strong Supervision

*Technical companion to Section 4 of "Automated Weak-to-Strong Researcher" (Anthropic, 2026)*

---

## Framing: The W2S Label-Noise View

All five methods share a common premise that the naive approach ignores.

The naive approach: treat weak labels `ŷ_w` as clean supervision and fine-tune the strong model directly. This achieves PGR ≈ 0.2 — barely above random.

The better view: `ŷ_w` is a **structured noisy observation** of the unknown true label `y*`. The noise is not random — it is correlated with instance difficulty, the weak model's confidence, and the strong model's internal representations. All five methods exploit this structure.

Common notation:
- `D = {(x_i, ŷ_w_i)}` — training set with weak labels
- `φ(x)` — frozen embeddings from the strong base model's final hidden layer
- `m(x)` — strong model's logit margin: `logit(A>B) − logit(B>A)` on a preference pair
- `ỹ_i ∈ [0,1]` — the corrected or soft label each method produces
- Goal: produce `ỹ_i` that better approximates `y*_i` than `ŷ_w_i` does

The strong model is not a passive student. Its representations, margins, and training dynamics are the primary denoising signal in all five methods.

---

## Method 1: CCS + Evolution Strategy Refinement (PGR = 0.93)

### First Principles

This method combines two independent ideas applied sequentially:

**Stage A — CCS (Contrastive Consistency Search, Burns et al. 2022):** A transformer that has internalized a binary claim should represent it in a consistent direction in activation space. Specifically, if we ask the model about claim `c` and its negation `¬c`, the internal representations should be "opposite" — and the difference should be the same regardless of surface phrasing. This means there exists a linear direction `w` in hidden state space such that `w · h(c) > 0` and `w · h(¬c) < 0`, reliably. Crucially, this direction can be found *without any labels*, by optimizing:

```
L_CCS(w) = ‖σ(h_pos · w) + σ(h_neg · w) − 1‖² + ‖σ(h_pos · w)(1 − σ(h_pos · w))‖²
            ───────────────────────────────────────   ─────────────────────────────────────
                    consistency term                           confidence term
```

The consistency term forces the probe to give opposite answers for `(x, ¬x)` pairs. The confidence term prevents the trivial solution of always predicting 0.5. The result is an unsupervised confidence score `c_i = |w · h(x_i)|` — how far example `i` is from the probe's decision boundary.

**Stage B — Evolution Strategy (ES):** Given an unsupervised fitness signal (swap-consistency), gradient-based training is not necessary — or even desirable. The LoRA parameter vector is treated as the search variable. ES perturbs it, evaluates fitness, and updates using a gradient estimate. This is appropriate here because:
1. Swap-consistency is not differentiable through the sampling process
2. LoRA initializations create a multimodal loss landscape; ES can escape local optima

Swap-consistency as fitness: a well-calibrated preference model should be symmetric — `P(A>B|x) ≈ 1 − P(B>A|x)`. Define:

```
fitness(θ) = E_x[−|P_θ(A>B|x) + P_θ(B>A|x) − 1|] + E_x[|P_θ(A>B|x) − 0.5|]
              ──────────────────────────────────────   ────────────────────────────
                     symmetry reward                        confidence reward
```

No weak labels. No ground truth. The fitness signal is purely structural.

**Why 16 seeds + trimmed mean?** ES is stochastic; different seeds reach different local optima. Aggregating 16 runs and trimming the top and bottom 2 in logit space reduces variance without collapsing to a single run's noise.

### Algorithm

The two stages are strictly sequential: CCS resamples the training data, then ES optimizes a LoRA initialized on that resampled data.

Per seed (×16):

1. Forward-pass all training examples through the frozen strong base model, collecting hidden states at each layer `l`: `{h_l(x_i)}`

2. Run CCS at each layer: optimize `w_l` to minimize `L_CCS` (no labels used). Select the layer `l*` where the probe achieves highest leave-one-out accuracy using the weak labels as a one-time alignment check.

3. Compute per-example CCS confidence: `c_i = |w_{l*} · h_{l*}(x_i)|`

4. Resample the training set using `c_i` as importance weights — high-CCS examples drawn more frequently, creating a cleaner training distribution

5. SGD warmup: train LoRA on the resampled data for 1 epoch (standard cross-entropy on weak labels). This initializes the ES search point.

6. ES optimization loop (200 iterations):
   - Sample `n=16` perturbation vectors `{ε_j}`, each a dict of tensors with the same shapes as LoRA parameters, scaled by `σ=0.01`
   - For each `ε_j`: apply `θ ← θ + ε_j`, evaluate `f_j = fitness(θ + ε_j)` on a minibatch, revert `θ ← θ − ε_j`
   - Normalize fitness scores: `f̂_j = (f_j − mean(f)) / std(f)`
   - ES update: `θ ← θ + (lr / (n · σ)) · Σ_j f̂_j · ε_j`

7. Final inference with swap-consistent voting: predict the label that is consistent across both orderings

Aggregate 16 seeds: compute logit of each model's preference probability, take trimmed mean (drop top and bottom 2 of 16), threshold at 0.

### Code Sketch

```python
import torch
import torch.nn.functional as F
import numpy as np

def ccs_probe(hidden_pos: torch.Tensor, hidden_neg: torch.Tensor, n_steps=1000):
    """
    Find linear probe direction via CCS objective (fully unsupervised).

    hidden_pos: [N, d] — hidden states for the positive framing (A>B)
    hidden_neg: [N, d] — hidden states for the negative framing (B>A)
    Returns probe direction w: [d]
    """
    w = torch.nn.Parameter(torch.randn(hidden_pos.shape[1]))
    opt = torch.optim.Adam([w], lr=1e-3)
    for _ in range(n_steps):
        p_pos = torch.sigmoid(hidden_pos @ w)
        p_neg = torch.sigmoid(hidden_neg @ w)
        consistency = ((p_pos + p_neg - 1) ** 2).mean()
        confidence = (p_pos * (1 - p_pos)).mean()
        (consistency + confidence).backward()
        opt.step(); opt.zero_grad()
    return w.detach()

def swap_consistency_fitness(model, batch_ab: dict, batch_ba: dict) -> float:
    """
    ES fitness: high when model is confident AND symmetric across orderings.
    No labels required.
    """
    with torch.no_grad():
        logits_ab = model(**batch_ab).logits[:, -1, :]   # [B, vocab]
        logits_ba = model(**batch_ba).logits[:, -1, :]
        p_ab = torch.softmax(logits_ab, dim=-1)[:, TOKEN_A]  # P(A>B)
        p_ba = torch.softmax(logits_ba, dim=-1)[:, TOKEN_A]  # P(A>B given reversed order)
        symmetry = -((p_ab + p_ba - 1) ** 2).mean()
        confidence = (p_ab - 0.5).abs().mean()
    return (symmetry + confidence).item()

def es_optimize_lora(model, eval_batch_ab, eval_batch_ba,
                     n_iters=200, n_samples=16, sigma=0.01, lr=0.01):
    """
    Gradient-free ES over LoRA parameters using swap-consistency as fitness.

    get_lora_params / apply_lora_delta are stubs — replace with your LoRA implementation.
    Standard pattern: iterate model.named_parameters() filtering 'lora_' prefix.
    """
    for _ in range(n_iters):
        # Sample n_samples perturbation *vectors* (one full set of lora param deltas each)
        perturbations = [
            {name: torch.randn_like(p) * sigma
             for name, p in get_lora_params(model).items()}
            for _ in range(n_samples)
        ]
        fitnesses = []
        for eps in perturbations:
            apply_lora_delta(model, eps)
            fitnesses.append(swap_consistency_fitness(model, eval_batch_ab, eval_batch_ba))
            apply_lora_delta(model, {k: -v for k, v in eps.items()})  # revert

        f = torch.tensor(fitnesses)
        f_hat = (f - f.mean()) / (f.std() + 1e-8)  # normalize

        # ES gradient estimate: θ += (lr / (n * σ)) * Σ_j f̂_j * ε_j
        for lora_name, lora_param in get_lora_params(model).items():
            grad_est = sum(f_hat[j] * perturbations[j][lora_name] for j in range(n_samples))
            lora_param.data += (lr / (n_samples * sigma)) * grad_est

def aggregate_seeds(seed_logits: list, trim=2) -> torch.Tensor:
    """Trimmed mean across 16 seed models in logit space."""
    stacked = torch.stack(seed_logits, dim=0)  # [16, N]
    sorted_logits, _ = torch.sort(stacked, dim=0)
    return sorted_logits[trim:-trim].mean(dim=0)  # [N]
```

### What Makes It Non-Obvious

The alien move is using **swap-consistency as a complete replacement for supervision**. After CCS resampling, the weak teacher is entirely discarded. The model improves by enforcing a structural invariant — preference judgments should not depend on which response is listed first — with no access to ground truth. Most researchers would have used weak labels to drive ES. This method doesn't.

---

## Method 2: EM Posterior (PGR = 0.78)

### First Principles

The **Dawid-Skene model** (1979) is the classic framework for learning from noisy annotators. The key assumption: each annotator has a fixed confusion matrix `P(ŷ | y*)`. Given multiple annotators, EM recovers both the confusion matrices and the true label distribution.

This method generalizes Dawid-Skene in one critical way: there is only one annotator (the weak model), but its noise rate is **instance-dependent**. Easy examples are labeled correctly; hard ones are not. The confusion matrix is not constant — it is a function of per-instance features:

```
P(ŷ_w = 1 | y* = 1, x) = σ(f_TPR(features(x)))   ← true positive rate, instance-specific
P(ŷ_w = 0 | y* = 0, x) = σ(f_TNR(features(x)))   ← true negative rate, instance-specific
```

Where `features(x)` are derived from the frozen strong model:
- **margin mean**: `m̄_i = mean over K templates of signed logit margin`
- **margin stability**: `σ_m_i = std dev of margin across templates` — low variance = strong model agrees with itself
- **weak confidence**: `max(P_w(0|x_i), P_w(1|x_i))`
- **weak/strong agreement**: `1` if `sign(m̄_i) == ŷ_w_i`, else `0`

The Bayesian posterior label is:
```
P(y* = 1 | ŷ_w, x) ∝ P(ŷ_w | y* = 1, x) · P(y* = 1 | x)
```
where the prior `P(y* = 1 | x) = σ(m̄_i)` is the strong model's raw confidence. The EM loop then alternates: train student on posteriors → re-estimate confusion matrices using student predictions → recompute posteriors.

### Algorithm

1. **Feature extraction** (frozen strong base model):
   - For each `x_i`, evaluate across `K` prompt templates (paper: "multiple templates"; K is unspecified — a reasonable default is 5) in both orderings
   - Compute `margin_mean_i`, `margin_std_i`, `weak_conf_i`, `agree_i`

2. **Initial pseudo-labels**: use strong model's argmax `(sign(margin_mean_i))` as proxy for `y*`

3. **Fit initial channel model** via logistic regression separately for TPR and TNR:
   - `clf_tpr`: `P(ŷ_w=1 | y*=1, features)` — fit on examples where strong pseudo-label = 1
   - `clf_tnr`: `P(ŷ_w=0 | y*=0, features)` — fit on examples where strong pseudo-label = 0

4. **Compute Bayesian posteriors**:
   - `prior_i = σ(margin_mean_i)`
   - `tpr_i = clf_tpr.predict_proba(features_i)[1]`
   - `fpr_i = 1 − clf_tnr.predict_proba(features_i)[1]`
   - `posterior_i = tpr_i · prior_i / (tpr_i · prior_i + fpr_i · (1 − prior_i))` for `ŷ_w=1`, symmetrically for `ŷ_w=0`
   - Apply temperature scaling to posteriors (not to the prior): `posterior_i^T = softmax(logit(posterior_i) / T)`

5. **EM Round 1**: train strong student on soft labels `{posterior_i}` for 2 epochs; extract student predictions `p_student_i`

6. **EM Round 2**: re-estimate channel model using `p_student_i > 0.5` as new proxy for `y*`; recompute posteriors; train final student

### Code Sketch

```python
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.linear_model import LogisticRegression

def extract_features(strong_model, dataset, weak_labels, n_templates=5):
    """Per-instance features from frozen strong model across multiple prompt templates."""
    N = len(dataset)
    features = np.zeros((N, 4))
    for i, (x, _) in enumerate(dataset):
        margins = []
        for t in range(n_templates):
            for sign, ordering in [(1, 'AB'), (-1, 'BA')]:
                prompt = build_prompt(x, ordering, template_id=t)
                with torch.no_grad():
                    logits = strong_model(prompt).logits[0, -1, :]
                margins.append(sign * (logits[TOKEN_A] - logits[TOKEN_B]).item())
        margin_mean = np.mean(margins)
        features[i] = [
            margin_mean,                                          # strong model margin
            np.std(margins),                                      # margin stability
            float(weak_model_confidence(x)),                      # weak confidence
            float(np.sign(margin_mean) == (2 * weak_labels[i] - 1))  # weak/strong agree
        ]
    return features

def fit_channel_model(features, weak_labels, pseudo_labels):
    """Fit instance-dependent noise channel P(weak | true, features)."""
    pos_mask = pseudo_labels == 1
    clf_tpr = LogisticRegression(max_iter=500).fit(features[pos_mask], weak_labels[pos_mask])
    clf_tnr = LogisticRegression(max_iter=500).fit(features[~pos_mask], 1 - weak_labels[~pos_mask])
    return clf_tpr, clf_tnr

def compute_posteriors(features, weak_labels, clf_tpr, clf_tnr, temperature=2.0):
    """Bayesian posterior P(y*=1 | ŷ_w, features) with posterior temperature scaling."""
    prior = torch.sigmoid(torch.tensor(features[:, 0], dtype=torch.float32))
    tpr = torch.tensor(clf_tpr.predict_proba(features)[:, 1], dtype=torch.float32)
    fpr = 1 - torch.tensor(clf_tnr.predict_proba(features)[:, 1], dtype=torch.float32)

    weak = torch.tensor(weak_labels, dtype=torch.float32)
    p_given_pos = tpr * prior / (tpr * prior + fpr * (1 - prior) + 1e-8)
    p_given_neg = (1 - fpr) * (1 - prior) / ((1 - fpr) * (1 - prior) + (1 - tpr) * prior + 1e-8)
    posteriors = torch.where(weak == 1, p_given_pos, p_given_neg)

    # Temperature scaling on posteriors (not on the prior)
    logits_post = torch.log(posteriors / (1 - posteriors + 1e-8))
    return torch.sigmoid(logits_post / temperature)

def em_round(model, dataloader, posteriors: torch.Tensor, n_epochs=2):
    """Train on soft labels using binary cross-entropy; return new model predictions."""
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    posterior_list = posteriors.tolist()
    for _ in range(n_epochs):
        for batch_x, batch_idx in dataloader:
            soft_y = torch.tensor([posterior_list[i] for i in batch_idx]).to(batch_x.device)
            logits = model(**batch_x).logits[:, -1, :]
            log_odds = logits[:, TOKEN_A] - logits[:, TOKEN_B]
            loss = F.binary_cross_entropy_with_logits(log_odds, soft_y)
            loss.backward(); optimizer.step(); optimizer.zero_grad()
    return get_model_predictions(model, dataloader)
```

### What Makes It Non-Obvious

Standard Dawid-Skene uses a single confusion matrix per annotator. The breakthrough here is recognizing that the strong model's own representations encode instance difficulty — so the noise rate can be *conditioned on the strong model's internal state*. An example where the strong model is highly confident and consistent across templates is labeled differently than one where the strong model wavers. The weak label's trustworthiness is not fixed; it is a function of the strong model's belief.

---

## Method 3: Overlap Density (PGR = 0.75) — The "Alien" Method

### First Principles

This method comes from a geometric intuition about representation space. The frozen strong model's embeddings `φ(x)` cluster semantically similar examples together. If a weak label is **locally consistent** with the embedding neighborhood — its k nearest neighbors tend to share the same label — then the label is likely correct. If the label is an outlier relative to its neighbors, it is likely noise.

The method formalizes this via 4 complementary signals, combined via z-score normalization without any learned combiner:

| # | Signal | What it measures |
|---|---|---|
| 1 | Cross-fitted logistic probe | Global linear separability: can `φ(x)` predict `ŷ_w`? |
| 2 | kNN label smoothness | Local consistency: do `x_i`'s neighbors share its weak label? |
| 3 | Local embedding density | Neighborhood compactness: is this region of space dense? |
| 4 | Mid-entropy preference | Avoid trivially easy or impossible examples |

Each signal is z-score normalized independently, then summed. No learnable combiner, no validation set, no hyperparameter tuning. The top 50% by combined score, balanced by class, are selected for fine-tuning.

### Algorithm

1. Extract frozen embeddings `φ(x_i) ∈ ℝ^d` for all `x_i ∈ D` (strong base model, final hidden layer)

2. **Signal 1** — Cross-fitted logistic probe (5-fold OOF):
   - Fit `LogisticRegression(φ, ŷ_w)` on each 4-fold training split, predict OOF probabilities
   - `s1_i = P_probe(ŷ_w_i | φ(x_i))` — probability the probe assigns to the actual weak label

3. **Signal 2** — kNN label smoothness (k=15):
   - Build nearest-neighbor index over `{φ(x_i)}`
   - `s2_i = fraction of x_i`'s k nearest neighbors with the same weak label as `x_i`

4. **Signal 3** — Local density:
   - `s3_i = 1 / (1 + mean Euclidean distance to k nearest neighbors)`
   - Denser neighborhoods → example lies in a well-populated region → more likely representative

5. **Signal 4** — Mid-entropy preference:
   - Uses OOF probe confidence (Signal 1's `oof_prob_i = P_probe(1 | φ(x_i))`) as an uncertainty proxy
   - *Note: the paper specifies "mid-entropy preference" without specifying which probability; using the OOF probe is a natural engineering choice*
   - `s4_i = 1 − |2 · oof_prob_i − 1|`  — peaks at `oof_prob=0.5` (maximum uncertainty/informativeness)

6. Z-score normalize each signal independently; `score_i = z(s1_i) + z(s2_i) + z(s3_i) + z(s4_i)`

7. Select top 50% by score, enforcing class balance (equal number from each class)

8. Fine-tune strong model on selected subset with weak labels

### Code Sketch

```python
import numpy as np
import faiss
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

def compute_overlap_density_scores(embeddings: np.ndarray, weak_labels: np.ndarray, k: int = 15):
    """
    embeddings: [N, d] — frozen strong base model embeddings
    weak_labels: [N]   — 0/1 weak labels
    Returns: scores [N]
    """
    N, d = embeddings.shape
    emb_f32 = embeddings.astype(np.float32)

    # Signal 1: 5-fold OOF logistic probe
    clf = LogisticRegression(max_iter=500)
    oof_probs = cross_val_predict(clf, embeddings, weak_labels, cv=5, method='predict_proba')
    s1 = oof_probs[np.arange(N), weak_labels]   # P(correct weak label class)
    oof_conf = oof_probs[:, 1]                   # P(label=1), used for Signal 4

    # Build kNN index
    index = faiss.IndexFlatL2(d)
    index.add(emb_f32)
    distances, neighbor_idx = index.search(emb_f32, k + 1)
    distances = distances[:, 1:]          # [N, k], exclude self
    neighbor_idx = neighbor_idx[:, 1:]   # [N, k]

    # Signal 2: kNN label smoothness
    neighbor_labels = weak_labels[neighbor_idx]   # [N, k]
    s2 = (neighbor_labels == weak_labels[:, None]).mean(axis=1)

    # Signal 3: local density (inverse mean neighbor distance)
    s3 = 1.0 / (1.0 + distances.mean(axis=1))

    # Signal 4: mid-entropy preference (peaks at maximum uncertainty)
    # Uses OOF probe confidence as uncertainty proxy (engineering interpretation of paper's
    # "mid-entropy preference" — paper does not specify which probability to use)
    s4 = 1.0 - np.abs(2.0 * oof_conf - 1.0)

    def zscore(x):
        return (x - x.mean()) / (x.std() + 1e-8)

    return zscore(s1) + zscore(s2) + zscore(s3) + zscore(s4)

def select_top_balanced(scores: np.ndarray, weak_labels: np.ndarray, top_fraction: float = 0.5):
    """Select top-scoring examples with equal class representation."""
    n_per_class = int(len(scores) * top_fraction) // 2
    selected = []
    for cls in [0, 1]:
        idx = np.where(weak_labels == cls)[0]
        top_idx = idx[np.argsort(scores[idx])[-n_per_class:]]
        selected.append(top_idx)
    return np.concatenate(selected)
```

### What Makes It Non-Obvious

The alien element is the **absence of a learned combiner**. Every data selection paper learns a quality predictor. Here, four geometrically motivated heuristics are z-score normalized and summed with equal weights. No training required. No held-out validation set needed to tune the combination. The AAR discovered that the structural geometry of the embedding manifold is sufficient — a finding that would surprise most researchers who would immediately reach for a learned reweighter.

---

## Method 4: MDL Curriculum (PGR = 0.68)

### First Principles

**Minimum Description Length (MDL)** formalizes Occam's razor in information-theoretic terms: the best model is the one that minimizes the total description length of the data and the model together. Applied to individual training examples: an example that a model can predict with high confidence requires few bits to describe — it is "compressible." An example near the decision boundary requires many bits — it is noisy or ambiguous.

The weak model's confidence `conf_i = max(P_w(0|x_i), P_w(1|x_i))` is a proxy for compressibility:
- `conf_i → 1.0`: the example is confidently labeled → likely correctly labeled → high signal, low noise
- `conf_i → 0.5`: the example is near the weak model's decision boundary → likely noisy or ambiguous

**Why not just filter low-confidence examples?** Hard filtering permanently discards examples that may carry useful signal for the noisy tail of the distribution. MDL curriculum instead *sequences* the exposure:

- **Phase 1** builds the correct prior from the compressible, clean core
- **Phase 2** uses that prior as regularization when extending to the full noisy data

The halved learning rate in Phase 2 is critical: it prevents the model from overwriting the Phase-1 patterns with gradient updates from the noisy tail.

### Algorithm

1. For each training example `x_i`, query the weak model to obtain `conf_i = max(P_w(0|x_i), P_w(1|x_i))`

2. Select `D_easy = {x_i : conf_i ≥ median(conf)}` — the top 50% most confident examples

3. **Phase 1**: Fine-tune strong model on `D_easy` for 2 epochs at learning rate `lr`
   - Standard cross-entropy on hard weak labels `ŷ_w_i`
   - Do not modify labels or apply any smoothing

4. **Phase 2**: Continue from Phase-1 checkpoint, training on the full `D` for 3 epochs at `lr/2`
   - Same loss, same labels, just the full dataset at half the learning rate

5. Return the Phase-2 checkpoint as the final model

### Code Sketch

```python
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset

def mdl_curriculum_train(model, dataset, weak_confidences: np.ndarray,
                          lr=2e-5, n_easy_epochs=2, n_full_epochs=3, batch_size=16):
    """
    Two-phase curriculum based on weak model confidence as an MDL proxy.

    weak_confidences: [N] — max(P_w(0|x), P_w(1|x)) for each example, precomputed
    """
    # Select easy (high-confidence) examples
    threshold = np.median(weak_confidences)
    easy_idx = np.where(weak_confidences >= threshold)[0].tolist()
    easy_loader = DataLoader(Subset(dataset, easy_idx), batch_size=batch_size, shuffle=True)
    full_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    # Phase 1: train on easy (high-confidence) examples
    model.train()
    for _ in range(n_easy_epochs):
        for batch_inputs, batch_labels in easy_loader:   # batch_labels: long tensor [B]
            logits = model(**batch_inputs).logits[:, -1, :][:, [TOKEN_A, TOKEN_B]]  # [B, 2]
            loss = F.cross_entropy(logits, batch_labels)
            loss.backward(); optimizer.step(); optimizer.zero_grad()

    # Phase 2: reduce LR, train on full data (preserves Phase-1 prior)
    for pg in optimizer.param_groups:
        pg['lr'] = lr / 2

    for _ in range(n_full_epochs):
        for batch_inputs, batch_labels in full_loader:
            logits = model(**batch_inputs).logits[:, -1, :][:, [TOKEN_A, TOKEN_B]]
            loss = F.cross_entropy(logits, batch_labels)
            loss.backward(); optimizer.step(); optimizer.zero_grad()

    return model
```

### What Makes It Non-Obvious

The simplicity is deceptive. The full implementation is 20 lines with no additional infrastructure — no noise model, no embeddings, no iterative relabeling. The MDL reframing converts an inference problem ("which labels are noisy?") into a scheduling problem ("which examples should be seen first?"). The AAR found this simple rescheduling alone is sufficient to reach PGR = 0.68, comfortably above all human baselines.

---

## Method 5: Epiplexity (PGR = 0.62)

### First Principles

"Epiplexity" is a term coined by the AAR. It operationalizes a distinction between two modes of model behavior on a training example:

- **Memorization**: the model sees a large loss drop across training passes — high loss on first encounter, low loss on last. The example contains structure the model can encode.
- **Noise**: the model shows near-zero loss drop — the example cannot be compressed. Loss fluctuates without a trend.

Formally:
```
epiplexity_i = L(x_i, ŷ_w_i, epoch=1) − L(x_i, ŷ_w_i, epoch=last)
```

High epiplexity → example is learnable → weak label probably correct → keep sharp label.
Low epiplexity → example is not learnable → weak label probably noisy → smooth toward 0.5.

This is used to calibrate **per-sample adaptive label smoothing**:
```
ỹ_i = (1 − ε_i) · soft_i + ε_i · 0.5
```
where `ε_i` is a function of rank-normalized epiplexity. The functional form `ε_i = (1 − r_i)^α` with convex curvature `α > 1` is an implementation interpretation — the paper specifies "convex curvature concentrating on the worst tail" without giving a closed form.

The **K-fold OOF** step generates soft pseudo-labels `soft_i` without a separate teacher: train K strong models each on K−1 folds, predict on the held-out fold. This avoids the chicken-and-egg problem of needing labels to generate better labels.

### Algorithm

1. **K-fold OOF soft labels** (K=5):
   - For each fold `k ∈ {0, ..., 4}`: train strong model on `D \ D_k`; predict soft probability `P(y=1|x_i)` for all `i ∈ D_k`
   - Collect OOF predictions: `soft_i = P_model_k(y=1|x_i)` for each held-out `i`

2. **Epiplexity probe pass**:
   - Initialize a fresh strong model (from pretrained weights); train on `{(x_i, soft_i)}` for `E` epochs
   - Record per-example losses: `loss_first_i` on the first encounter (epoch 1), `loss_last_i` on the last encounter (epoch E)
   - `epiplexity_i = loss_first_i − loss_last_i`

3. **Adaptive label smoothing**:
   - Rank-normalize: `r_i = rank(epiplexity_i) / N` — ranks in [0, 1], high rank = high epiplexity = learnable
   - Bottom 40%: `ε_i = (1 − r_i)^α` (α=2.0 gives convex decay; interpret as plan's approximation, not paper's exact formula)
   - Top 60%: `ε_i = 0` (keep sharp OOF labels)
   - `ỹ_i = (1 − ε_i) · soft_i + ε_i · 0.5`

4. **Swap augmentation**: for each `(x_i, ỹ_i)`, add `(swap(x_i), 1 − ỹ_i)` — flipping the comparison order should flip the label

5. Train final strong model on augmented dataset `{(x_i, ỹ_i)} ∪ {(swap(x_i), 1 − ỹ_i)}`

### Code Sketch

```python
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset

def oof_soft_labels(model_weights_path: str, dataset, n_folds=5, batch_size=16) -> np.ndarray:
    """
    K-fold OOF: generate soft pseudo-labels without a separate teacher model.

    model_weights_path: path to pretrained base model — each fold loads fresh weights
    """
    N = len(dataset)
    fold_size = N // n_folds
    oof_probs = np.zeros(N)

    for k in range(n_folds):
        val_idx = list(range(k * fold_size, min((k + 1) * fold_size, N)))
        train_idx = [i for i in range(N) if i not in val_idx]

        model = load_pretrained_model(model_weights_path)  # fresh weights per fold
        train_fold(model, Subset(dataset, train_idx), batch_size=batch_size)

        with torch.no_grad():
            for batch_inputs, _, batch_idx in DataLoader(
                    Subset(dataset, val_idx), batch_size=batch_size):
                logits = model(**batch_inputs).logits[:, -1, :]
                log_odds = logits[:, TOKEN_A] - logits[:, TOKEN_B]  # [B]
                probs = torch.sigmoid(log_odds).cpu().numpy()
                for j, global_i in enumerate(batch_idx):
                    oof_probs[global_i] = probs[j]

    return oof_probs

def compute_epiplexity(model_weights_path: str, dataset, soft_labels: np.ndarray,
                       n_epochs=3, batch_size=16) -> np.ndarray:
    """Record per-sample loss drop across training epochs (first vs. last encounter)."""
    N = len(dataset)
    loss_first = np.full(N, np.nan)
    loss_last = np.full(N, np.nan)
    seen = np.zeros(N, dtype=bool)

    model = load_pretrained_model(model_weights_path)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    for _ in range(n_epochs):
        for batch_inputs, _, batch_idx in DataLoader(dataset, batch_size=batch_size, shuffle=True):
            soft_y = torch.tensor([soft_labels[i] for i in batch_idx], dtype=torch.float32)
            logits = model(**batch_inputs).logits[:, -1, :]
            log_odds = logits[:, TOKEN_A] - logits[:, TOKEN_B]   # [B]
            per_sample_loss = F.binary_cross_entropy_with_logits(
                log_odds, soft_y.to(log_odds.device), reduction='none')

            for j, i in enumerate(batch_idx):
                if not seen[i]: loss_first[i] = per_sample_loss[j].item(); seen[i] = True
                loss_last[i] = per_sample_loss[j].item()

            per_sample_loss.mean().backward()
            optimizer.step(); optimizer.zero_grad()

    return loss_first - loss_last   # epiplexity: large = learnable structure

def adaptive_smooth(epiplexity: np.ndarray, soft_labels: np.ndarray,
                    alpha=2.0, bottom_frac=0.4) -> np.ndarray:
    """
    Per-sample label smoothing: noisy examples smoothed toward 0.5.

    ε_i = (1 − r_i)^alpha for bottom bottom_frac; 0 otherwise.
    Note: (1−r)^alpha is this implementation's interpretation of the paper's
    "convex curvature" — the paper does not specify the exact functional form.
    """
    ranks = np.argsort(np.argsort(epiplexity)) / len(epiplexity)   # normalized to [0,1]
    eps = np.where(ranks < bottom_frac, (1.0 - ranks) ** alpha, 0.0)
    return (1.0 - eps) * soft_labels + eps * 0.5

def add_swap_augmentation(dataset, smoothed_labels: np.ndarray) -> list:
    """Double the dataset with consistency-enforcing swapped pairs."""
    augmented = [(x, label) for (x, _), label in zip(dataset, smoothed_labels)]
    augmented += [(swap_orderings(x), 1.0 - label)
                  for (x, _), label in zip(dataset, smoothed_labels)]
    return augmented
```

### What Makes It Non-Obvious

The AAR coined a new term for a concept that doesn't exist in the standard ML vocabulary. The core insight: instead of asking "is this example noisy?" (which requires ground-truth labels), ask "does the model compress this example during training?" (which requires only the loss trajectory). Label quality estimation becomes a **dynamics problem** — entirely observable from training logs, with no external signal required. The K-fold OOF step further removes the dependency on any separate teacher model.

---

## Closing Synthesis

All five methods reject the naive assumption that weak labels are a clean signal. Each one uses a different property of the strong model's structure to separate signal from noise:

| Method | PGR | Denoising signal exploited |
|---|---|---|
| CCS + ES Refinement | 0.93 | Unsupervised truth direction in hidden activation space |
| EM Posterior | 0.78 | Instance-level noise channel conditioned on strong model features |
| Overlap Density | 0.75 | Geometric consistency between weak labels and embedding manifold |
| MDL Curriculum | 0.68 | Weak confidence as proxy for label compressibility |
| Epiplexity | 0.62 | Loss trajectory as proxy for example learnability |

None required access to ground-truth labels during training. All use the strong model's own structure to self-denoise the weak supervision — operationalizing the W2S framing: the strong model already "knows" more than the weak supervisor, if you can extract the right signal.

**The human baseline was PGR = 0.23 after 7 days.** The AAR reached PGR = 0.97 in 5 days across 9 parallel runs. The gap is not explained by any single algorithmic insight. It is the product of iteration velocity: the ability to test a hypothesis against the eval API, observe the result, diagnose the failure mode from training logs, and redirect — all within hours rather than days. The methods above are what that velocity produced.
