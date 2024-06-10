import { create } from "zustand";

export const useModalStore = create((set) => ({
	modals: [
		{ name: "fichaAntecedentes", status: false },
		{ name: "crearDevolucion", status: false },
		{ name: "crearLiquidacion", status: false },
		{ name: "historicoLiquidacion", status: false },
	],
	hideAllModals: () =>
		set((state) => {
			let modalsParse = [...state.modals];
			for (let index = 0; index < modalsParse.length; index++) {
				modalsParse[index].status = false;
			}
			return { modals: modalsParse };
		}),
	showOneModal: (name) =>
		set((state) => {
			let modalsParse = [...state.modals];
			for (let index = 0; index < modalsParse.length; index++) {
				if (modalsParse[index].name == name) {
					modalsParse[index].status = true;
				}
			}
			return { modals: modalsParse };
		}),
}));
