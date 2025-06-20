const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const handleLogin = async (e) => {
  e.preventDefault();
  console.log("Form submitted");
  try {
    const response = await fetch(`${BACKEND_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await response.json();
    localStorage.setItem("user_id", data.user_id);
    console.log(data);

    navigate("/dashboard");
  } catch (error) {
    setErrorMessage(error.message);
  }
};
