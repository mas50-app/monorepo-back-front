// import React, { useMemo } from 'react';
// import { useState, useEffect } from 'react';
// import {useMutation} from "@tanstack/react-query";
// import {createPermiso, deletePermiso, getPermisos, getTiposPersonal, updatePermiso} from "../../apis/calls.js";
// import BasicGrill from "../../components/BasicGrill.jsx";
// import {successMessagePopUp} from "../../components/alerts.jsx";
//
// export const Permisos = () => {
//
//     const [permisos, setPermisos] = useState(null);
//     const [refresh, setRefresh] = useState(false);
//
//
//     useEffect(() => {
//         getDataPermisos.mutate()
//     }, [refresh]);
//
//
//
//     const crearPermiso = useMutation({
//         mutationFn: createPermiso,
//         onSuccess: (result) => {
//             console.log("Creado", result)
//             setRefresh(e=>!e)
//             successMessagePopUp({title:"Terminado" ,message:"Registro guardado exitosamente"})
//         },
//         onError: (error) => {
//             console.log("error", error);
//         },
//     });
//
//     const actualizarPermiso = useMutation({
//         mutationFn: updatePermiso,
//         onSuccess: (result) => {
//             console.log("Creado", result)
//             setRefresh(e=>!e)
//             successMessagePopUp({title:"Terminado" ,message:"Registro actualizado exitosamente"})
//         },
//         onError: (error) => {
//             console.log("error", error);
//         },
//     });
//
//     const eliminarPermiso = useMutation({
//         mutationFn: deletePermiso,
//         onSuccess: (result) => {
//             console.log("Creado", result)
//             setRefresh(e=>!e)
//             successMessagePopUp({title:"Terminado" ,message:"Registro eliminado exitosamente"})
//         },
//         onError: (error) => {
//             console.log("error", error);
//         },
//     });
//
//     const getDataPermisos = useMutation({
//         mutationFn: getPermisos,
//         onSuccess: (result) => {
//             console.log("Permisos", result)
//             setPermisos(result)
//         },
//         onError: (error) => {
//             console.log("error", error);
//         },
//     });
//
//     const fieldsPerm = [
//         {
//             field: "cod_permiso",
//             label: "Cod Permiso",
//             required: true,
//             type: "text",
//             show: false,
//             inTable: true
//         },
//         {
//             field: "desc_permiso",
//             label: "Permiso",
//             required: true,
//             type: "text",
//             show: true,
//             inTable: true
//         },
//     ]
//
//
//     return (
//         <div className="flex flex-row h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2 overflow-hidden">
//                 {permisos &&
//                     <div className="mt-4 w-full h-full">
//                         <label className="p-4">Permisos: {permisos?.length}</label>
//                         <BasicGrill
//                             fields={fieldsPerm}
//                             tableData={permisos}
//                             parentName="¨Permisos"
//                             SaveFunc={crearPermiso.mutate}
//                             EditFunc={actualizarPermiso.mutate}
//                             DeleteFunc={eliminarPermiso.mutate}
//                         />
//                     </div>
//                 }
//         </div>
//     );
// };
//
