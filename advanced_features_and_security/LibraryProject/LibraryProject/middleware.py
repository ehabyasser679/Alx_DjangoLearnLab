"""
Custom middleware for Content Security Policy (CSP) headers.

This middleware implements CSP to help prevent XSS attacks by controlling
which resources (scripts, styles, images, etc.) can be loaded by the browser.

Security: CSP is a defense-in-depth measure that works alongside Django's
built-in XSS protections (template auto-escaping).
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    """
    Content Security Policy middleware.
    
    Adds CSP headers to all responses to prevent XSS attacks by restricting
    which resources can be loaded and executed by the browser.
    
    Security Benefits:
    - Prevents inline script execution (unless explicitly allowed)
    - Restricts resource loading to trusted domains
    - Prevents data exfiltration via unauthorized connections
    - Reduces risk of XSS attacks even if other protections fail
    """
    
    def process_response(self, request, response):
        """
        Add Content Security Policy headers to the response.
        
        CSP directives:
        - default-src: Fallback for other directives
        - script-src: Controls which scripts can be executed
        - style-src: Controls which stylesheets can be loaded
        - img-src: Controls which images can be loaded
        - font-src: Controls which fonts can be loaded
        - connect-src: Controls which URLs can be loaded via fetch/XHR
        - frame-ancestors: Prevents embedding in frames (clickjacking)
        """
        # Build CSP header from settings
        csp_parts = []
        
        # Default source (fallback for other directives)
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_parts.append(f"default-src {settings.CSP_DEFAULT_SRC}")
        
        # Script sources (JavaScript)
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_parts.append(f"script-src {settings.CSP_SCRIPT_SRC}")
        
        # Style sources (CSS)
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_parts.append(f"style-src {settings.CSP_STYLE_SRC}")
        
        # Image sources
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_parts.append(f"img-src {settings.CSP_IMG_SRC}")
        
        # Font sources
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_parts.append(f"font-src {settings.CSP_FONT_SRC}")
        
        # Connect sources (fetch, XHR, WebSocket)
        if hasattr(settings, 'CSP_CONNECT_SRC'):
            csp_parts.append(f"connect-src {settings.CSP_CONNECT_SRC}")
        
        # Frame ancestors (prevents clickjacking)
        if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
            csp_parts.append(f"frame-ancestors {settings.CSP_FRAME_ANCESTORS}")
        
        # Add CSP header if any directives are configured
        if csp_parts:
            csp_value = "; ".join(csp_parts)
            response['Content-Security-Policy'] = csp_value
        
        return response

