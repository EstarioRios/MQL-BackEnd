function accessTokenFinder() {
  const accesstokenStorage = localStorage.getItem("access_token");
  const accesstokenSession = sessionStorage.getItem("access_token");
  if (accesstokenStorage) {
    return { accessToken: accesstokenStorage, error: null };
  } else if (accesstokenSession) {
    return { accessToken: accesstokenSession, error: null };
  } else {
    return { accessToken: null, error: "no_authenticated".toString() };
  }
}

async function signup(email, phone_number, password, first_name, last_name) {
  const params = [email, phone_number, password, first_name, last_name];
  if (!params.every()) {
    return { error: "no_params", msg: null, status: null };
  }
  const body = {
    email: email,
    phone_number: phone_number,
    password: password,
    first_name: first_name,
    last_name: last_name,
  };
  const { accessToken, error } = accessTokenFinder();
  if (error) {
    return { error: error, msg: null, status: null, user: null };
  }
  const response = await fetch("/api/signup/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken.toString(),
    },
    body: JSON.stringify(body),
  });

  const result = response.json();
  if (!response.ok) {
    return { error: result.error, msg: null, status: result.status };
  } else {
    return {
      error: null,
      msg: result.message.toString(),
      user: result.user,
      tokens: result.tokens,
      status: result.status,
    };
  }
}

async function login() {
  const { accessToken, error } = accessTokenFinder();
  if (error) {
    return { error: error, msg: null, status: null, user: null };
  }
  const response = await fetch("/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken.toString(),
    },
  });

  const result = response.json();
  if (!response.ok) {
    return { error: result.error, msg: null, status: result.status };
  } else {
    return {
      error: null,
      msg: result.success.toString(),
      user: result.user,
      user_type: result.user_type,
      status: result.status,
    };
  }
}

async function manualLogin(email, password, remember) {
  const params = [email, password];
  if (!params.every()) {
    return {
      error: "no params",
      msg: null,
      status: null,
      user: null,
      tokens: null,
      user_type: null,
    };
  }
  const body = { email: email, password: password, remember: remember };

  const response = await fetch("/api/manual-login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const result = response.json();
  if (!response.ok) {
    return {
      error: result.error,
      msg: null,
      status: result.status,
      user: null,
      tokens: null,
      user_type: null,
    };
  } else {
    if (remember === true) {
      return {
        error: null,
        msg: result.success,
        status: result.status,
        user: result.user,
        tokens: result.tokens,
        user_type: result.user_type,
      };
    }
    if (remember === false) {
      return {
        error: null,
        msg: result.success,
        status: result.status,
        user: result.user,
        tokens: null,
        user_type: result.user_type,
      };
    }
  }
}

async function createAdmin(
  first_name,
  last_name,
  email,
  password,
  phone_number
) {
  const params = [first_name, last_name, email, password, phone_number];
  if (!params.every()) {
    return { error: "no params", msg: null, status: null, user: null };
  }

  const body = {
    first_name: first_name,
    last_name: last_name,
    email: email,
    password: password,
    phone_number: phone_number,
  };

  const { accessToken, error } = accessTokenFinder();
  if (error) {
    return { error: error, msg: null, status: null, user: null };
  }

  const response = await fetch("", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken.toString(),
    },
    body: JSON.stringify(body),
  });

  const result = response.json();

  if (!response.ok) {
    return {
      error: result.error,
      msg: null,
      status: result.status,
      user: null,
    };
  } else {
    return {
      error: null,
      msg: result.msg,
      status: result.status,
      user: result.user,
    };
  }
}

async function subOrder(title, description, tools_description) {
  const params = [title, description, tools_description];
  if (!params.every()) {
    return { error: "no params", msg: null, status: null, order: null };
  }
  const { accessToken, error } = accessTokenFinder();
  if (error) {
    return { error: error, msg: null, status: null, order: null };
  }

  const body = {
    title: title,
    description: description,
    tools_description: tools_description,
  };

  const response = await fetch("/api/sub-order /", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken.toString(),
    },
    body: JSON.stringify(body),
  });
  const result = response.json();

  if (!response.ok) {
    return {
      error: result.error,
      msg: null,
      status: result.status,
      order: null,
    };
  } else {
    return {
      error: null,
      msg: result.msg,
      status: result.status,
      order: result.order,
    };
  }
}
