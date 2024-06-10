const API = import.meta.env.VITE_API;

export const baseGet = async (ruta, token) => {
	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				authorization: "Bearer " + token,
			},
		});
		const data = await res.json();
		if (res.status != 200) return null;
		return data;
	} catch (e) {
		return null;
	}
};

export const basePost = async (ruta, token, cuerpo) => {
	let header =
		token == ""
			? { "Content-Type": "application/json" }
			: {
					"Content-Type": "application/json",
					authorization: "Bearer " + token,
			  };

	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "POST",
			headers: header,
			body: JSON.stringify(cuerpo),
		});
		const data = await res.json();
		if (res.status != 200 && res.status != 201) {
			return null
		}
		else{
			return data;
		}
	} catch (e) {
		console.log("error", e);
		return null;
	}
};

export const basePut = async (ruta, token, cuerpo) => {
	let header =
		token == ""
			? { "Content-Type": "application/json" }
			: {
					"Content-Type": "application/json",
					authorization: "Bearer " + token,
			  };

	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "PUT",
			headers: header,
			body: JSON.stringify(cuerpo),
		});
		const data = await res.json();
		if (res.status != 200 && res.status != 201) {
			return null
		}
		else{
			return data;
		}
	} catch (e) {
		console.log("error", e);
		return e;
	}
};

export const baseDelete = async (ruta, token, cuerpo) => {
	let header =
		token == ""
			? { "Content-Type": "application/json" }
			: {
					"Content-Type": "application/json",
					authorization: "Bearer " + token,
			  };
	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "DELETE",
			headers: header,
			body: JSON.stringify(cuerpo),
		});
		const data = await res.json();
		if (res.status != 200) {
			console.log("ELMINANDO", data)
			return null
		}
		else{
			return data;
		}
	} catch (e) {
		console.log("error", e);
		return null;
	}
};



export const multiPartPost = async (ruta, token, cuerpo) => {
	let header =
		token == ""
			? { }
			: {
				authorization: "Bearer " + token,
			};

	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "POST",
			headers: header,
			body: cuerpo,
		});
		const data = await res.json();
		if (res.status != 200 && res.status != 201) {
			return null
		}
		else{
			return data;
		}
	} catch (e) {
		console.log("error", e);
		return null;
	}
};


export const multiPartPut = async (ruta, token, cuerpo) => {
	let header =
		token == ""
			? { }
			: {
				authorization: "Bearer " + token,
			};

	try {
		const res = await fetch(`${API}${ruta}`, {
			method: "PUT",
			headers: header,
			body: cuerpo,
		});
		const data = await res.json();
		if (res.status != 200 && res.status != 201) {
			return null
		}
		else{
			return data;
		}
	} catch (e) {
		console.log("error", e);
		return null;
	}
};

export async function basePostImageDataUrl(ruta, token, cuerpo) {
	let header =
		token == ""
			? { "Content-Type": "application/json" }
			: {
				"Content-Type": "application/json",
				authorization: "Bearer " + token,
			};
	const response = await fetch(`${API}${ruta}`, {
		method: "POST",
		headers: header,
		body: JSON.stringify(cuerpo),
	});
	if (response.status != 200){
		return null
	}
	const blob = await response.blob();
	return new Promise((resolve) => {
		const reader = new FileReader();
		reader.onloadend = () => resolve(reader.result);
		reader.readAsDataURL(blob);
	});
}