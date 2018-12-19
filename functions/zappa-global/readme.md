To deploy a Lambda function globally (to primary location as it's configured):

1. Open `zappa_settings.json` and change all bucket names. They all have to be unique
2. Run `zappa deploy --all`
