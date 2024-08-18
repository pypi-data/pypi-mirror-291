// src/Login.tsx
import React, {useState} from 'react';
import {useMutation} from "@tanstack/react-query";
import {Features} from "../features";
import {useNavigate} from "react-router-dom";
import {Helmet} from "react-helmet-async";


function LoginPage() {
    const navigate = useNavigate()
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const {mutate, isLoading, isError} = useMutation({
        mutationFn: ({username, password}: {
            username: string,
            password: string
        }) => Features.login(username, password),
        onSuccess: () => {
            navigate('/dataset')
        }
    });

    const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        mutate({username, password});
    };

    return (
        <>
            <Helmet>
                <title> login | dataset.sh </title>
            </Helmet>

            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-500 to-green-500">
                <div className="bg-orange-50 p-8 rounded shadow-lg w-96 ">
                    <h2 className="text-2xl font-bold mb-4">Login</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label className="block text-gray-700 font-bold mb-2" htmlFor="username">
                                Username
                            </label>
                            <input
                                className="w-full px-3 py-2 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
                                type="text"
                                id="username"
                                placeholder="Username"
                                value={username}
                                onChange={handleUsernameChange}
                                required
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 font-bold mb-2" htmlFor="password">
                                Password
                            </label>
                            <input
                                className="w-full px-3 py-2 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
                                type="password"
                                id="password"
                                placeholder="Password"
                                value={password}
                                onChange={handlePasswordChange}
                                required
                            />
                        </div>
                        <button
                            className="bg-green-400 text-gray-700 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline hover:bg-blue-600"
                            type="submit"
                            disabled={isLoading}
                        >
                            {isLoading ? 'Logging in...' : 'Login'}
                        </button>
                        {isError && <p className="text-red-500 mt-2">Login failed. Please try again.</p>}
                    </form>
                </div>
            </div>
        </>
    );
};

export default LoginPage;
