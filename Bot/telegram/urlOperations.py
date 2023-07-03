import re    # for regex


def remove_urls_from_message(message):
    # Define a regular expression pattern to match URLs
    url_regex = r'(https?://\S+)'
    
    # Remove URLs from the message using the pattern
    message_without_urls = re.sub(url_regex, '', message)
    
    return message_without_urls



def url_parser(message):
    # Define a regular expression to match URLs
    url_regex = r'(https?://\S+)'

    parsed_response = message  # Initialize with the original message text
    parsed_urls = set()  # Set to store unique URLs

    # Check if the message contains URLs
    urls = re.findall(url_regex, message)
    for url in urls:
        # Check if the URL has already been included in the message
        if url not in parsed_urls:
            parsed_urls.add(url)
            parsed_response += '\n' + url  # Append the unique URL to the parsed response

    return parsed_urls