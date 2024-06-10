import React, { useEffect } from "react";
import useLoginCookie from "../utils/loginCookies.js";
import { login } from "../apis/calls";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import {getTokenData} from "../utils/tokenData.js";

const Login = () => {
	const [isLoggedIn, setLoginCookie, removeLoginCookie] = useLoginCookie();
	const navigate = useNavigate();

	const handleSubmit = async (event) => {
		event.preventDefault();
		const formData = {};
		for (let element of event.target.elements) {
			if (element.name) {
				formData[element.name] = element.value;
			}
		}
		loginMutation.mutate(formData);
	};

	const loginMutation = useMutation({
		mutationFn: login,
		onSuccess: (result) => {
			setLoginCookie(result.token);
			navigate("/home");
		},
		onError: (response) => {
			console.log("error llamada", response.response.data);
		},
	});

	useEffect(() => {
		(async () => {
			const token = await getTokenData()
			if (token === null){
				return
			}
			navigate("/home")
		})()
	}, []);

	return (
		<section className="h-screen">
			<div className="container px-6 py-12 h-full">
				<div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
					<div className="mb-12 ">
						<img
							src="/logo_color.svg"
							height={10}
							width={10}
							className="w-48 m-5"
							alt="Phone image"
						/>
					</div>
					<div className="md:w-8/12 lg:w-5/12 lg:ml-20">
						<form onSubmit={handleSubmit}>
							<div className="mb-6">
								<input
									type="text"
									className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-purple-900 focus:outline-none"
									placeholder="usuario"
									name="login_personal"
								/>
							</div>

							<div className="mb-6">
								<input
									type="password"
									className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-purple-900 focus:outline-none"
									placeholder="contraseña"
									name="contrasena"
								/>
							</div>

							<button
								type="submit"
								className="inline-block px-7 py-3 bg-purple-600  text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-purple-900 hover:shadow-lg focus:bg-purple-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out w-full"
								data-mdb-ripple="true"
								data-mdb-ripple-color="light"
							>
								Iniciar sesión
							</button>
						</form>
					</div>
				</div>
			</div>
		</section>
	);
};

export default Login;
