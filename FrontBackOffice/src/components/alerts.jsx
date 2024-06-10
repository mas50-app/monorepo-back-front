import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import {useEffect, useState} from "react";
import {useRef} from "react";

export const errorMessagePopUp = ({title, message}) => {
    const MySwal = withReactContent(Swal);
    MySwal.fire({
        icon: "error", title: title, text: message,
        // footer: '<a href="">Why do I have this issue?</a>',
    });
};

export const infoMessagePopUp = ({title, message}) => {
    const MySwal = withReactContent(Swal);
    MySwal.fire({
        icon: "info", title: title, text: message,
        // footer: '<a href="">Why do I have this issue?</a>',
    });
};

export const successMessagePopUp = ({title, message}) => {
    const MySwal = withReactContent(Swal);
    MySwal.fire({
        icon: "success", title: title, text: message,
        // footer: '<a href="">Why do I have this issue?</a>',
    });
};

export const questionMessagePopUp = ({title, functionOnConfirm}) => {
    const MySwal = withReactContent(Swal);
    MySwal.fire({
        icon: "question",
        title: title,
        showClass: {
            popup: "animate_animated animate_fadeInDown"
        },
        hideClass: {
            popup: "animate_animated animate_fadeOutUp"
        },
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: "Si ",
        confirmButtonColor: "#2CE7B7",
        denyButtonText: "No",
        customClass: {
            actions: "my-actions",
            confirmButton: "btn btn-success",
            denyButton: "btn btn-danger"
        }
    }).then((result) => {
        if (result.isConfirmed) {
            functionOnConfirm();
        }
    });
};

export const loadingPopup = (title, func, setIsLoading) => {
    setIsLoading(true)
    const MySwal = withReactContent(Swal);

    const timeout = setTimeout(() => {
        MySwal.close(); // Cerrar SweetAlert después de 5 segundos
    }, 5000);

    MySwal.fire({
        title: `Cargando ${title}`,
        html: "Por favor espere unos segundos...",
        allowEscapeKey: false,
        allowOutsideClick: false,
        showConfirmButton: false,
        didOpen: () => {
            MySwal.showLoading();
        }
    });

    func().then(() => {
        clearTimeout(timeout); // Si la llamada a la API se completa antes de 5 segundos, cancelar el tiempo de espera y cerrar SweetAlert.
        setIsLoading(false)
        MySwal.close();
    }).catch(() => {
        clearTimeout(timeout); // Si se produce un error, cancelar el tiempo de espera y cerrar SweetAlert.
        setIsLoading(false)
        MySwal.close();
    });
};


export const SimpleLoadingPopup = () => {
    const MySwal = withReactContent(Swal);
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const popup = MySwal.fire({
            title: "Cargando Datos",
            html: "Por favor espere unos segundos...",
            allowEscapeKey: false,
            allowOutsideClick: false,
            showConfirmButton: false,
            didOpen: () => {
                MySwal.showLoading(MySwal.getCancelButton());
            }
        });

        // Cerrar el popup cuando el componente se desmonte
        return() => {
            setIsVisible(false);
            popup.close();
        };
    }, []);

    return isVisible ? null : <></>;
};


export const FormPopup = async (desdeRef, hastaRef) => {
    const MySwal = withReactContent(Swal);
    const result = await MySwal.fire({
        title: 'Seleccione rango de fecha',
        html: <div className="flex flex-col w-full h-full justify-center items-center gap-2">
            <div className="flex flex-row justify-center items-center gap-2">
                <label htmlFor="desde">Desde</label>
                <input className="border roudnded p-2" type="date" id="desde"
                    ref={desdeRef}/>
            </div>
            <div className="flex flex-row justify-center items-center gap-2">
                <label htmlFor="hasta">Hasta</label>
                <input className="border roudnded p-2" type="date" id="hasta"
                    ref={hastaRef}/>
            </div>
        </div>,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Descargar',
        confirmButtonColor: 'purple',
        preConfirm: () => {
            return {desde: desdeRef.current.value, hasta: hastaRef.current.value}
        }
    });
	console.log("RESULT", result);
    if (result.isConfirmed) {
        return {desde: result.value.desde, hasta: result.value.hasta};
    } else {
        return {desde: null, hasta: null};
    }
}
