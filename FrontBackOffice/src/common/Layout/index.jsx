import React from "react";
import HeaderComponente from "./header";
import Sidebar from "./sidebar";
import Footer from "./footer";

const LayoutD = ({ children }) => {
	return (
		<div className="flex flex-col max-h-screen h-screen w-screen overflow-hidden">
			<HeaderComponente />
			<div className="flex flex-row overflow-hidden h-full w-full">
				<Sidebar />
				<div className="flex flex-col overflow-hidden justify-between h-full w-full">
					<div className="px-2 pt-2 pb-2 pr-5 h-full w-full flex flex-col overflow-hidden overflow-y-auto">
						{children}
					</div>

					<Footer />
				</div>
			</div>
		</div>
	);
};
export default LayoutD;
