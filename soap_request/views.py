from django.shortcuts import render
from django.http import JsonResponse

import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['POST'])
def soap_request(request):
    if request.method == "POST":
        soap_request_body = request.body.decode('utf-8')
        json_response = soap_to_json_converter(soap_request_body)

        return JsonResponse(
            {
                "responseObject": {
                    "code": 1,
                    'data': json_response
                },
                "statusCode": "00",
                "successful": True,
                "statusMessage": "Success"                        
            }
        )
    else:
        message = f"Wrong request type. This is a 'POST' Request! "
        return JsonResponse(
            {
                "responseObject": {
                    "code": -1,
                    'data': message
                },
                "statusCode": "99",
                "successful": False,
                "statusMessage": "Fail"                        
            }
        )

def soap_to_json_converter(soap_request: str) -> dict:
    """
    Converts a SOAP request to a JSON-like dictionary.

    Args:
        soap_request (str): A SOAP request as an XML string.

    Returns:
        dict: A dictionary representing the SOAP request.
    """
    def parse_element(element):
        """Recursively parses an XML element into a dictionary."""
        parsed = {}
        # Add attributes
        if element.attrib:
            parsed.update({f"@{k}": v for k, v in element.attrib.items()})
        # Add text content
        if element.text and element.text.strip():
            parsed["#text"] = element.text.strip()
        # Add child elements
        for child in element:
            child_parsed = parse_element(child)
            if child.tag not in parsed:
                parsed[child.tag] = child_parsed
            else:
                if not isinstance(parsed[child.tag], list):
                    parsed[child.tag] = [parsed[child.tag]]
                parsed[child.tag].append(child_parsed)
        return parsed

    root = ET.fromstring(soap_request)
    return {root.tag: parse_element(root)}