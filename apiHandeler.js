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

async function subScore(user_id_code, score_title, score_value) {
  const { accessToken, error } = accessTokenFinder();
  if (error) {
    return { error: error, msg: null };
  }
  const params = [user_id_code, score_title, score_value];
  if (!params.every()) {
    return { error: "no_params", msg: null, status: result.status };
  }
  const body = {
    user_id_code: user_id_code,
    score_title: score_title,
    score_value: score_value,
  };

  const response = await fetch("/api/score/submit/", {
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
      status: result.status,
    };
  }
}
