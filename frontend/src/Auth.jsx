import { useState } from "react";

import { supabase } from "./supabaseClient";

function Auth({ setSession }) {

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  // ---------------------------------------------------
  // SIGN UP
  // ---------------------------------------------------

  const signUp = async () => {

    setLoading(true);

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      alert(error.message);
    } else {
      alert("Signup successful. Check email verification.");
    }

    setLoading(false);
  };

  // ---------------------------------------------------
  // LOGIN
  // ---------------------------------------------------

  const signIn = async () => {

    setLoading(true);

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {

      alert(error.message);

    } else {

      setSession(data.session);
    }

    setLoading(false);
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">

        <h1 className="text-3xl font-bold text-center mb-6">
          ChemEduAI Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-3 rounded w-full mb-4"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-3 rounded w-full mb-6"
        />

        <div className="flex gap-4">

          <button
            onClick={signIn}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded w-full"
          >
            Login
          </button>

          <button
            onClick={signUp}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded w-full"
          >
            Sign Up
          </button>

        </div>

        {loading && (
          <p className="mt-4 text-center">
            Processing...
          </p>
        )}

      </div>

    </div>
  );
}

export default Auth;