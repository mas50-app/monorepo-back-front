import React from "react";
import Modal_Base from "./modal_base";

function Modal_splash({ estado }) {
	return (
		<Modal_Base showModal={estado}>
			<div className="inline-block align-center bg-white">
				<div className="w-full h-full ">
					<img
						src="/logo_color.svg"
						height={10}
						width={10}
						className="w-48 m-5 animate-pulse"
						alt="Phone image"
					/>
				</div>
			</div>
		</Modal_Base>
	);
}

export default Modal_splash;
