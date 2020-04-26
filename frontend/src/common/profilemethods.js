// Import CSRT TOKEN & Credentials
import { CSRF_TOKEN } from "./csrf_token.js";

// function handleResponse(response) {
//   if (response.status === 204) {
//     return "";
//   } else if (response.status === 404) {
//     return null;
//   } else {
//     return response.json();
//   }
// }

// API FUNCTIONS
class APICall {
  // Make an HTTP GET Request
  async get(url) {
    const response = await fetch(url);
    const resData = await response.json();
    return resData;
  }

  // Make an HTTP POST Request
  async post(url, data) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        "X-CSRFTOKEN": CSRF_TOKEN
      },
      body: JSON.stringify(data)
    });

    const resData = await response.json();
    return resData;
  }

  // Make an HTTP Update Request
  async put(url, data) {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
        "X-CSRFTOKEN": CSRF_TOKEN
      },
      body: JSON.stringify(data)
    });

    const resData = await response.json();
    return resData;
  }

  // NOTE THAT THE DATA FOR THIS NEEDS TO COME IN AS FORMDATA
  async changePhoto(url, data) {
    const response = await fetch(url, {
      method: "PATCH",
      headers: {
        "X-CSRFTOKEN": CSRF_TOKEN
      },
      body: data
    });

    const resData = await response.json();
    return resData;
  }
}

function syncProfileInLocalStorage(userData) {
  // Does this really need to be stringified if it's coming straight from API?
  localStorage.setItem("userDataSerialized", JSON.stringify(userData));
}

// KEEP AS COMMENTImportant Variables In UserData:
// let userData = {
//    username: String,
//    photo: String,
//    avatar: String,
//    biography: String,
//    country: String,
//    geoloc: String,
//    lativeLanguage: String,
//    learningLanguage: Array,
//    learningTopics: Array,
//    addedDate: String,
//    points: Number,
//    TODO: reverse lookup of LIKES
//    TODO: reverse lookup of FOLLOWERS & FOLLOWING
//    TODO: reverse lookup of COMMENTS & RESPONSES & MESSAGES
// }

// Pull userData from LocalStorage
// Example = this.userData = getUserDataLocal();
function getLocalUserData() {
  let userData;
  if (localStorage.getItem("userDataSerialized") === null) {
    userData = Object;
  } else {
    userData = JSON.parse(localStorage.getItem("userDataSerialized"));
  }
  return userData;
}

// Sync UserData to LocalStorage
// Example = this.userData = syncProfileInLocalStorage (userData);

// Retrieve User Profile from Server
function retrieveProfileAPI() {
  APICall.get(`api/users/profile/get/`)
    // We must ensure that object that is returned over API is Complete (may need to fix the JSON format)
    .then(resdata => syncProfileInLocalStorage(resdata))
    .catch(err => console.log(err));
  // SHOULD THIS BE RETURNED SOMEHOW?
}

// Update User Profile Preferences on Server
function updateProfilePreferencesAPI(userData) {
  // The Django serializer will handle which data gets a partial update
  APICall.put(`api/users/profile/update/`, userData)
    .then(resdata => console.log(resdata))
    .catch(err => console.log(err));
  // first syncLocalStorage
  // propogate LocaltoAPI
  // Update Languages, Topics, & Bio
}

// Change Password
function changePasswordAPI(password1, password2) {
  APICall.post(`/api/rest-auth/password/change/`, {
    new_password1: password1,
    new_password2: password2
  })
    .then(resdata => console.log(resdata))
    .catch(err => console.log(err));
}

// Change Username
function changeUsernameAPI(username) {
  APICall.post(`/api/users/changeusername/`, "POST", { username: username })
    .then(resdata => console.log(resdata))
    .catch(err => console.log(err));
}

// Change Image
function changePhotoAPI(data) {
  // NOTE THAT THE DATA FOR THIS NEEDS TO COME IN AS FORMDATA
  APICall.changePhoto(`/api/users/profileimageupload/`, data)
    .then(resdata => console.log(resdata))
    .catch(err => console.log(err));
}

// TODO Update User Profile in Local Storage
// TODO Increase User Points
// This should probably be done on the Django server using a set of variables for different point values
// Should probably issue an API call every time the user does something that could change the profile...
// It should be worth considering that a user's points could be updated as a result of another user's actions
// Should further consider where to put things like messages, likes, and other issues associated with a user

export {
  changePhotoAPI,
  getLocalUserData,
  retrieveProfileAPI,
  updateProfilePreferencesAPI,
  changePasswordAPI,
  changeUsernameAPI
};
