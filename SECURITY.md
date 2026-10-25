# Local API Configuration and Historical Exposure

The weather and location-time code reads OPENWEATHERMAP_API_KEY from the local process environment. A missing or blank value raises a clear configuration error before an HTTP request is made. The .env.example file is a reference only; the application does not load .env files or require a new dotenv dependency.

For PowerShell, set the value privately in the shell where the assistant will run:

```powershell
$env:OPENWEATHERMAP_API_KEY = '<your-own-key>'
Set-Location 'Nova Software'
python main.py
```

For a POSIX shell:

```sh
export OPENWEATHERMAP_API_KEY='<your-own-key>'
cd 'Nova Software'
python main.py
```

Use a credential you control; do not paste it into issues, commits, screenshots or test fixtures. Shell command history may retain an entered value; use your normal private environment/secret configuration method where appropriate. The app still requires its existing speech, desktop and NLP dependencies and local devices. This change does not supply the missing dependency manifest or establish a successful desktop run.

Weather requests use HTTPS. Error messages added here avoid printing request URLs/objects, which can contain credentials. Tests use dummy strings and mocked HTTP; no live key is needed.

## Outstanding Remediation

Previously committed values remain exposed through Git history and potentially forks, caches, logs, artifacts or existing deployments. Removing them from current source does not revoke them. The credential owner must revoke/rotate the exposed values and review usage with the provider. No key was validated, rotated or revoked by this change. Git history, repository visibility, releases and deployments were not changed.

The existing desktop automation/authentication prototype has broader security and reproducibility limitations outside this credential-removal change. It is not presented as production security software.
