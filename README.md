# Usage

Ensure python is installed.
Download all the files including utils folder

1. `pip install requirements.txt`
2. Run the following in terminal:
```
export API_KEY="your-api-key"
export PROJECT_KEY="your-project-key"
export ENVIRONMENT_KEY="your-environment-key"
```
3. `python3 main.py` (replace main.py with 1main-xxx or 2main-xxx etc)

## What happens now?
When you run the script using the above instructions mainly 1main-paylater-project-usage.py, it will:
1. Grab a list of feature flags in the project you defined
2. For each flag, get the last 30 days of usage using [this call](https://apidocs.launchdarkly.com/tag/Account-usage-(beta)/#operation/getEvaluationsUsage)
3. Create `output.txt` in the project's root directory listing the flags, with the flag's aggregate usage

## Caveats
Please double check before trusting this too much. :) It was whipped together on a plane VERY quickly with little regard to code quality.# LaunchDarklyScripts
