import { CSRF_TOKEN } from "./csrf_token.js";

function handleResponse(response) {
  if (response.status === 204) {
    return "";
  } else if (response.status === 404) {
    return null;
  } else {
    return response.json();
  }
}

function apiFileService(endpoint, method, data) {
  const config = {
    method: method || "POST",
    body: data,
    headers: {
      // "Content-Type": "multipart/form-data",
      "X-CSRFTOKEN": CSRF_TOKEN
      // "Authorization": "Token "
    }
  };
  return fetch(endpoint, config)
    .then(handleResponse)
    .catch(error => console.log(error));
}

export { apiFileService };
