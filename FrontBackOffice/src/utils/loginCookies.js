import { jwtVerify } from "jose";
import Cookies from "js-cookie";
const SECRET = import.meta.env.VITE_SECRET;
import { useEffect, useState } from "react";

const useLoginCookie = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(null);

	useEffect(() => {
		(async () => {
			const loginCookie = Cookies.get("token");
			if (loginCookie) {
				try {
					const decodedToken = await verifyToken(loginCookie);
					setIsLoggedIn(decodedToken);
				} catch (error) {
					setIsLoggedIn(null);
				}
			} else {
				setIsLoggedIn(null);
			}
		})();
	}, []);

	const verifyToken = async (token) => {
		const payload = await jwtVerify(token, new TextEncoder().encode(SECRET));
		return payload;
	};

	const setLoginCookie = (value) => {
		Cookies.set("token", `${value}`);
		setIsLoggedIn(true);
	};

	const removeLoginCookie = () => {
		Cookies.remove("token", null);
		setIsLoggedIn(false);
	};

	return [isLoggedIn, setLoginCookie, removeLoginCookie];
};
export default useLoginCookie;
