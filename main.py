import os
import logging as log
import google.cloud.logging as logging
import psycopg2

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(message='Server is up!'), 200

@app.route('/api/auth/apikey', methods=['GET'])
def get_auth_apikey():
    return jsonify(message='Congratulations. You have completed apikey auth.',
                   auth='apikey'), 200

@app.route('/api/auth/bearer', methods=['GET'])
def get_auth_sabearer():
    return jsonify(message='Congratulations. You have completed service account bearer auth.',
                   auth='service account bearer'), 200

@app.errorhandler(400)
def bad_request_error(e):
    return jsonify(code=400,
                   message='Bad request',
                   detailedMessage='{}'.format(e)), 400


@app.errorhandler(404)
def not_found_error(e):
    return jsonify(code=404,
                   message='Path not found',
                   detailedMessage='{}'.format(e)), 404


@app.errorhandler(405)
def method_not_allowed_error(e):
    return jsonify(code=405,
                   message='Method not allowed',
                   detailedMessage='{}'.format(e)), 405


@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify(code=500,
                   message='Internal server error',
                   detailedMessage='{}'.format(e)), 500


@app.route("/")
def hello_world():
    logging_client = logging.Client()
    logging_client.setup_logging()
    name = os.environ.get("NAME", "World")
    log.info(f"hello NAME: {name}")
    return "Hello {}!".format(name)

@app.route("/db", methods=["GET"])
def hello_db():
    logging_client = logging.Client()
    logging_client.setup_logging()
    log.info("hello_db called")
    db_user = os.environ.get("DB_USER")
    log.info(f"DB_USER: {db_user}") 
    db_password = os.environ.get("DB_PASSWORD")
    log.info(f"DB_PASSWORD: {db_password}") 
    db_host = os.environ.get("DB_INSTANCE_IP")
    log.info(f"DB_INSTANCE_IP: {db_host}") 
    db_hostname = os.environ.get("DB_INSTANCE_NAME")
    log.info(f"DB_INSTANCE_NAME: {db_hostname}") 
    db_database = os.environ.get("DB_DATABASE")
    log.info(f"DB_DATABASE: {db_database}") 
    sslmode = os.environ.get("DB_SSL_MODE")
    log.info(f"DB_SSL_MODE: {sslmode}") 
    #disable, require, verify-ca
    
    if sslmode == "verify_full":
        log.info("Connection to DB with TLS enabled") 
        relative_path_to_ssl_ca_cert = 'db-certs/'+db_hostname+'/cacert.crt'
        log.info(f"CACERT PATH: {relative_path_to_ssl_ca_cert}") 
        relative_path_to_ssl_client_cert = 'db-certs/'+db_hostname+'/client-cert.crt'
        log.info(f"Client cert: PATH: {relative_path_to_ssl_ca_cert}") 
        relative_path_to_ssl_client_key = 'db-certs/'+db_hostname+'/client-key.pem'
        log.info(f"Client Key PATH: {relative_path_to_ssl_ca_cert}") 
        log.info(f"Current directory PATH: {os.getcwd()}") 
        SSL_ROOT_CERT = os.path.join(os.getcwd(), relative_path_to_ssl_ca_cert )
        root_cert_exists = os.path.exists(SSL_ROOT_CERT)
        log.info(f"CACERT Exists: {root_cert_exists}") 
        log.info(f"CACERT PATH ABSOLUTE: {SSL_ROOT_CERT}") 
        SSL_CLIENT_CERT = os.path.join(os.getcwd() , relative_path_to_ssl_client_cert )
        client_cert_exists = os.path.exists(SSL_CLIENT_CERT)
        log.info(f"Client Cert Exists: {client_cert_exists}") 
        log.info(f"SSL_CLIENT_CERT PATH ABSOLUTE: {SSL_CLIENT_CERT}") 
        SSL_CLIENT_KEY = os.path.join(os.getcwd(), relative_path_to_ssl_client_key )
        client_key_exists = os.path.exists(SSL_CLIENT_KEY)
        log.info(f"Client Key Exists: {client_key_exists}") 
        log.info(f"SSL_CLIENT_KEY PATH ABSOLUTE: {SSL_CLIENT_KEY}") 
        connection = psycopg2.connect(user=db_user,
                                    password=db_password,
                                    host=db_host,
                                    port="5432",
                                    database=db_database,
                                    sslmode='require',
                                    sslcert=SSL_CLIENT_CERT,
                                    sslkey=SSL_CLIENT_KEY,
                                    sslrootcert=SSL_ROOT_CERT)
    else:    
        log.info("Connection to DB") 
        connection = psycopg2.connect(user=db_user,
                                    password=db_password,
                                    host=db_host,
                                    port="5432",
                                    database=db_database)
    
    log.info(f"Connection created: {connection}") 
    cursor = connection.cursor()
    log.info("Connected to database") 
    print(cursor.execute("select 2;"))
    print(cursor.execute("select 3;"))
    print(cursor.execute("select 4;"))
    print(cursor.execute("select CURRENT_TIMESTAMP;"))
    cursor_records = cursor.fetchall()
    log.info("Executed queries") 
    log.info("Print each row and it's columns values")
    for row in cursor_records:
        print("Id = ", row[0])
    return "DB "

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))