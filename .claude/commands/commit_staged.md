Use current staged changes to commit. Do not add more files. Do not add Generated with Claude and Co-Authored-By: Claude.

Generate git commit message following conventional commit format with proper line width constraints:
- Title: under 50 characters
- Description: wrap lines at 72 characters

## Conventional Commit Types

**Allowed commit types:**

- **feat**: Add/modify features (new functionality)
- **fix**: Bug fixes (fixing defects in code)
- **docs**: Documentation changes (README, comments, etc.)
- **style**: Code formatting changes (whitespace, formatting, missing semicolons, etc. - no logic changes)
- **refactor**: Code restructuring (neither new features nor bug fixes)
- **perf**: Performance improvements (code changes that improve performance)
- **test**: Adding missing tests (when adding tests only)
- **chore**: Build process or auxiliary tool changes (maintenance tasks)
  - Note: updating build tasks, modifying .gitignore, etc.; no production code changes
- **revert**: Reverting previous commits (format: revert: type(scope): subject)

## Example Format

```
feat: implement time-series splitting strategies

- Add data split module with multiple strategies (random, time-series,
  stratified, group, leave-one-out)
- Add configuration classes (SplitConfig, CrossValidationConfig) for
  split parameters
- Add timestamp columns support in base training config
- Add split_config.yaml for time-based data splitting settings
```