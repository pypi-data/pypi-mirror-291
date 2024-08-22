from dnscli.dns import AliApi

access_key_id = "LTAI5tHissrhRrGTFuhvjnu4"
access_key_secret = "28QyrWLNRjvysluCTk2EdxBUOMPksM"

api = AliApi(
    secret_id=access_key_id,
    secret_key=access_key_secret
)


record_list = api.get_record(domain="wfugui.com", sub_domain=None, record_type=None, line=None)
print(record_list)
