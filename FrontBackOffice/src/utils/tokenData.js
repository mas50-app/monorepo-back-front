import Cookies from "js-cookie";
import { verifyToken } from "../apis/calls";

export const getTokenData = async () => {
	const token = Cookies.get("token");
	return await verifyToken(token);
};
