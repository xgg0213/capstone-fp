import Cookies from 'js-cookie';

export async function csrfFetch(url, options = {}) {
  // set options.method to 'GET' if there is no method
  options.method = options.method || 'GET';
  // set options.headers to an empty object if there is no headers
  options.headers = options.headers || {};

  // if the options.method is not 'GET', then set the "Content-Type" header to
  // "application/json", and set the "XSRF-TOKEN" header to the value of the
  // "XSRF-TOKEN" cookie
  if (options.method.toUpperCase() !== 'GET') {
    options.headers['Content-Type'] =
      options.headers['Content-Type'] || 'application/json';
    options.headers['XSRF-Token'] = Cookies.get('XSRF-TOKEN');
  }

  // call the default window's fetch with the url and the options passed in
  const res = await window.fetch(url, options);

  // if the response status code is 401 (Unauthorized), handle it specially
  if (res.status === 401) {
    // Try to restore CSRF token first
    try {
      await restoreCSRF();
      
      // Try the request again with the new CSRF token
      options.headers['XSRF-Token'] = Cookies.get('XSRF-TOKEN');
      const retryRes = await window.fetch(url, options);
      
      // If retry is successful, return the response
      if (retryRes.ok) {
        return retryRes;
      }
      
      // If retry still fails with 401, then it's a real auth issue
      if (retryRes.status === 401) {
        const error = new Error('Authentication required');
        error.status = 401;
        error.authError = true;
        throw error;
      }
      
      // For other errors, continue with normal error handling
      if (retryRes.status >= 400) throw retryRes;
      
      return retryRes;
    } catch (retryError) {
      // If CSRF restoration fails or retry fails, throw auth error
      if (retryError.authError) throw retryError;
      
      const error = new Error('Authentication required');
      error.status = 401;
      error.authError = true;
      throw error;
    }
  }
  
  // if the response status code is 400 or above, then throw an error with the
  // error being the response
  if (res.status >= 400) throw res;

  // if the response status code is under 400, then return the response to the
  // next promise chain
  return res;
}

export async function restoreCSRF() {
  const response = await fetch('/api/csrf/restore', {
    credentials: 'include' // Important for cookies
  });
  
  if (response.ok) {
    // Extract the CSRF token from the response cookies
    const csrfToken = Cookies.get('XSRF-TOKEN');
    if (!csrfToken) {
      console.error('Failed to get CSRF token from cookies');
    }
    return response;
  } else {
    console.error('Failed to restore CSRF token:', response.status);
    throw new Error('Failed to restore CSRF token');
  }
}