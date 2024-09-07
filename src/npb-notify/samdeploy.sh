#sam delete
sam build
sam deploy \
  --stack-name npb-notify-poc \
  --parameter-overrides \
    TagName=poc \
    WebhookUrlSlack=$NPB_WEBHOOK_URL_SLACK_PRD \
    BaseDomainName=$NPB_BASE_DOMAIN_NAME \
