from boto import sqs
import json
import time

from django.conf import settings
from pointstracker import models

def _put_json(o):
  conn = sqs.connect_to_region(settings.PT_SQS_REGION,
      aws_access_key_id=settings.PT_AWS_ACCESS_KEY_ID,
      aws_secret_access_key=settings.PT_AWS_SECRET_ACCESS_KEY)
  queue = conn.get_queue(settings.PT_QUEUE_NAME)

  m = sqs.message.Message()
  m.set_body(json.dumps(o))
  queue.write(m)

def put_message(ty, params):
  obj = {'timestamp': time.time(), 'message_type': ty, 'params': params}
  _put_json(obj)

def _put_rewards_balance_refresh(revision_id):
  put_message('rewards_balance_refresh', {'rewards_program_account_revision_id':revision_id})

def refresh_rewards_balance(account):
  rev = models.RewardsProgramAccountRevision(account=account, pending=1)
  rev.save()
  _put_rewards_balance_refresh(rev.id)  
