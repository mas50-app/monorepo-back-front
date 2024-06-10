export function formatFloat(num) {
	return num.toLocaleString("es-CL",{
		style: "currency",
		currency: "CLP" // aquí puedes cambiar la moneda por cualquier otra que necesites
	})
}
