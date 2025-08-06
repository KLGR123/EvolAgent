"""
Response parser utility for handling LLM API responses.
Provides JSON parsing, field validation, and error handling capabilities.
"""

import re
import json
import logging
import json_repair
from typing import Dict, List, Any
from ..config import config


class ResponseParseError(Exception):
    """Custom exception for response parsing errors."""
    
    def __init__(self, message: str, role: str, content: str = "", original_error: Exception = None):
        self.role = role
        self.content = content
        self.original_error = original_error
        super().__init__(f"{role}: {message}")


class ResponseParser:
    """
    A utility class for parsing and validating LLM API responses.
    
    Features:
    - JSON extraction from markdown code blocks
    - Robust JSON parsing with error repair
    - Configuration-driven field validation
    - Role-based response validation
    - Comprehensive error handling and logging
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize the response parser.
        
        Args:
            logger: Optional logger instance for debugging and error reporting
        """
        self.logger = logger
        self._json_pattern = r'```json\s*\n?(.*?)\n?```'
    
    def parse_response(self, response: str, role: str) -> Dict[str, Any]:
        """
        Parse the JSON response from LLM API with enhanced error handling.
        
        Args:
            response: The response from the LLM API, a string
            role: The role of the node making the request
            
        Returns:
            The parsed and validated JSON as a dictionary
            
        Raises:
            ResponseParseError: If parsing or validation fails
        """
        
        if self.logger:
            self.logger.debug(f"Parsing JSON response for {role}: {response[:200]}...")
        
        # Step 1: Extract JSON content
        json_content = self._extract_json_content(response)
        
        # Step 2: Parse JSON with repair capabilities
        parsed_json = self._parse_json_with_repair(json_content, role)
        
        # Step 3: Validate and normalize data type
        parsed_json = self._validate_data_type(parsed_json, role)
        
        # Step 4: Validate and fix role field
        self._validate_and_fix_role_field(parsed_json, role)
        
        # Step 5: Validate and fix required fields based on configuration
        self._validate_and_fix_required_fields(parsed_json, role)
        
        if self.logger:
            self.logger.debug(f"Successfully parsed response for {role}")
        
        return parsed_json
    
    def _extract_json_content(self, response: str) -> str:
        """
        Extract JSON content from response, handling markdown code blocks.
        """

        matches = re.findall(self._json_pattern, response, re.DOTALL | re.IGNORECASE)
        
        if matches:
            json_content = matches[0].strip()
            if self.logger:
                self.logger.debug("Found JSON in markdown code block")
        else:
            json_content = response.strip()
            if self.logger:
                self.logger.debug("Using entire response as JSON content")
                
        return json_content
    
    def _parse_json_with_repair(self, json_content: str, role: str) -> Dict[str, Any]:
        """
        Parse JSON content with automatic repair capabilities.
        json_repair is a library for repairing JSON data. 
        Thank you to the author: https://github.com/mverleg/json_repair
        """

        try:
            parsed_json = json_repair.loads(json_content)
            if self.logger:
                self.logger.debug("JSON parsed successfully using json_repair")
            return parsed_json
            
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger.error(f"JSON parsing failed for {role}: {str(e)}")
                self.logger.debug(f"Failed JSON content: {json_content}")
            raise ResponseParseError(
                f"JSON parsing failed: {str(e)}", 
                role, 
                json_content, 
                e
            )
    
    def _validate_data_type(self, parsed_json: Any, role: str) -> Dict[str, Any]:
        """
        Validate and convert parsed JSON to dictionary format.
        """

        if not isinstance(parsed_json, dict):
            if isinstance(parsed_json, list) and len(parsed_json) > 0:
                parsed_json = parsed_json[0]
                if self.logger:
                    self.logger.debug("Parsed a list of dicts, taking the first one")
                    
                if not isinstance(parsed_json, dict):
                    raise ResponseParseError(
                        f"Invalid JSON format: expected dict, got {type(parsed_json)}", 
                        role
                    )
            else:
                if self.logger:
                    self.logger.error(f"Invalid JSON format for {role}: {parsed_json}")
                raise ResponseParseError(
                    f"Invalid JSON format: expected dict, got {type(parsed_json)}", 
                    role
                )
        
        return parsed_json
    
    def _validate_and_fix_role_field(self, parsed_json: Dict[str, Any], expected_role: str) -> None:
        """
        Validate and fix the role field in parsed JSON.
        
        Args:
            parsed_json: Parsed JSON dictionary (modified in place)
            expected_role: Expected role value
        """

        if "role" not in parsed_json:
            if self.logger:
                self.logger.warning(f"Missing 'role' field in response, setting to {expected_role}")
            parsed_json["role"] = expected_role
        elif parsed_json["role"] != expected_role:
            if self.logger:
                self.logger.warning(
                    f"Role mismatch: got '{parsed_json['role']}', expected '{expected_role}', correcting it"
                )
            parsed_json["role"] = expected_role
    
    def _validate_and_fix_required_fields(self, parsed_json: Dict[str, Any], role: str) -> None:
        """
        Validate and provide default values for required fields based on node role.
        Uses configuration-driven approach for better maintainability.
        
        Args:
            parsed_json: Parsed JSON dictionary (modified in place)
            role: Node role for field validation
        """
        
        required_fields = config.get_node_required_fields(role)
        default_values = config.get_node_field_defaults(role)
        
        if not required_fields:
            if self.logger:
                self.logger.debug(f"No field validation configuration found for role: {role}")
            return
        
        for field in required_fields:
            if field not in parsed_json:
                default_value = default_values.get(field, f"Missing {field}")
                if self.logger:
                    self.logger.warning(f"Missing '{field}' field in {role} response, setting default value")
                parsed_json[field] = default_value
                
        if self.logger:
            self.logger.debug(f"Field validation completed for {role} with {len(required_fields)} required fields")
    
    def get_supported_roles(self) -> List[str]:
        """
        Get list of supported roles with field validation configuration.
        
        Returns:
            List of role names that have field validation configuration
        """

        required_fields_config = config.get('nodes.required_fields', {})
        return list(required_fields_config.keys())
    
    def get_role_required_fields(self, role: str) -> List[str]:
        """
        Get required fields for a specific role.
        
        Args:
            role: Role name
            
        Returns:
            List of required field names
        """
        return config.get_node_required_fields(role)
    
    def get_role_field_defaults(self, role: str) -> Dict[str, str]:
        """
        Get default values for fields of a specific role.
        
        Args:
            role: Role name
            
        Returns:
            Dictionary mapping field names to default values
        """
        return config.get_node_field_defaults(role)


# Convenience function for quick parsing
def parse_llm_response(response: str, role: str, logger=None) -> Dict[str, Any]:
    """
    Convenience function for parsing LLM responses.
    
    Args:
        response: Raw response string from LLM
        role: Role of the requesting node
        logger: Optional logger instance
        
    Returns:
        Parsed and validated response dictionary
        
    Raises:
        ResponseParseError: If parsing fails
    """
    parser = ResponseParser(logger)
    return parser.parse_response(response, role) 