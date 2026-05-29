import axios from 'axios';

// const waste_url = 'http://127.0.0.1:5000/waste';

// export const fetchWasteItems = async () => {
//     const response = await axios.get(waste_url);
//     return response.data;
//};
//-------------------------------------------------------------------

const loginUrl = 'http://127.0.0.1:5000/auth';

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${loginUrl}/login`, {
      username,
      password,
    });

    if (response.data.role) {
      localStorage.setItem('userRole', response.data.role);
    }
    console.log("Login Response Data:", response.data); //  Debugging response data


    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message || 'Login failed');
    } else {
      throw new Error('Network error, please try again');
    }
  }
};
//-------------------------------------------------------------------