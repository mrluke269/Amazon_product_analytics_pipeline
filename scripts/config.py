RAPIDAPI_KEY = '187d7b0d2fmshb642a21912d2dbbp130898jsn0533211e9491'
RAPIDAPI_HOST = 'real-time-amazon-data.p.rapidapi.com'




from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Read the private key file
with open('C:\\Users\\Admin\\.ssh\\snowflake_key.p8', 'rb') as key_file:
    private_key_pem = key_file.read()

# Convert to the format Snowflake needs
private_key = serialization.load_pem_private_key(
    private_key_pem,
    password=None,  # Since you said no passphrase
    backend=default_backend()
)

# Serialize to DER format
my_snowflake_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

snowflake_config = {
    "user": "luketrmai",
    "account": "jfspetv-wgb43135",
    "private_key": my_snowflake_private_key,
    "warehouse": "compute_wh",
    "database": "raw",
    "schema": "amazon_product",
}

snowflake_table = "product_details" 
