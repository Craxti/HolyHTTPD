import json
import logging
import asyncio
import concurrent.futures
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read config file
with open('config.json') as f:
    config = json.load(f)

# Configure logger
logging.basicConfig(filename='logs/access.log', level=logging.INFO)

# Define thread pool executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=config['max_workers'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info('Received POST request from %s', request.remote_addr)
        # Process POST request asynchronously
        asyncio.ensure_future(handle_post_request(request))
        return 'OK', 200

    logging.warning('Received GET request from %s', request.remote_addr)
    # Process GET request asynchronously
    asyncio.ensure_future(handle_get_request(request))
    return '', 200


async def handle_post_request(request):
    # Process POST request
    try:
        data = await loop.run_in_executor(executor, request.get_json)
        # Add processing of received data here
        logging.info('Processed POST request from %s', request.remote_addr)
        
        # Example: Assuming the received data is a JSON object
        # You can access the data and perform any required operations
        if 'key' in data:
            value = data['key']
            # Perform some processing using the value
            
        # Example: Assuming you want to return a response
        response_data = {'message': 'Data processed successfully'}
        return jsonify(response_data), 200
        
    except Exception as e:
        logging.warning('Error processing POST request from %s: %s', request.remote_addr, str(e))
        # Example: Return an error response
        error_data = {'error': 'Failed to process the data'}
        return jsonify(error_data), 500

async def handle_get_request(request):
    # Process GET request
    try:
        # Add processing of received data here
        response_data = {}
        response_data['message'] = 'Processed GET request'
        response_data['client_ip'] = request.remote_addr
        response_data['user_agent'] = request.user_agent.string

        format_type = request.args.get('format', 'json')
        if format_type == 'json':
            # Example: Perform additional processing on the response_data before returning JSON
            # response_data['additional_field'] = 'Some value'
            return jsonify(response_data)
        else:
            # Example: Perform additional processing on the response_data before returning a string
            # response_data['additional_field'] = 'Some value'
            return str(response_data)

    except Exception as e:
        logging.warning('Error processing GET request from %s: %s', request.remote_addr, str(e))
        # Example: Return an error response
        error_data = {'error': 'Failed to process the request'}
        return jsonify(error_data), 500


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run(debug=config['debug'], host=config['host'], port=config['port'])
