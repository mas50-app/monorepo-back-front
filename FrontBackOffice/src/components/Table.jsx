import React, { forwardRef, useEffect, useMemo, useRef, useState } from "react";
import ReactDOMServer from "react-dom/server";
import {
	useGlobalFilter,
	usePagination,
	useSortBy,
	useTable,
	useRowSelect,
} from "react-table";
import { GlobalFilter } from "./GlobalFilter.jsx";
import * as XLSX from "xlsx/xlsx.mjs";
import { RiFileExcel2Line } from "react-icons/ri";
import { formatDate } from "../utils/dateFormat.js";

export function Table({
	COLUMNS,
	data,
	hiddenColumns,
	parentName,
	onRowSelect,
	filterGlobal = true,
	pagination = true
}) {
	const [menu, setMenu] = useState(null);

	const columns = useMemo(() => COLUMNS, []);

	const tableInstance = useTable(
		{
			columns: columns,
			data,
			initialState: {
				hiddenColumns: hiddenColumns ? hiddenColumns : [],
			},
		},
		useGlobalFilter,
		useSortBy,
		usePagination,
		useRowSelect
	);

	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		page,
		nextPage,
		previousPage,
		prepareRow,
		canPreviousPage,
		canNextPage,
		pageOptions,
		pageCount,
		gotoPage,
		state,
		setPageSize,
		setGlobalFilter,
		rows,
		selectedFlatRows,
		state: { selectedRowIds },
	} = tableInstance;

	useEffect(() => {
		if (onRowSelect != null) {
			onRowSelect(selectedFlatRows);
		}
	}, [onRowSelect, selectedFlatRows]);

	const { globalFilter, pageIndex, pageSize } = state;

	function exportToExcel() {
		const columnFieldMap = {};
		tableInstance.columns.forEach((column) => {
			if (column.id) {
				columnFieldMap[column.id] = column.Header;
				console.log("Excel", column.id, column.Header);
			}
		});

		const filteredData = [];

		tableInstance.data.forEach((dat) => {
			const filDat = {};
			Object.keys(dat).map((key) => {
				if (Object.keys(columnFieldMap).includes(key)) {
					filDat[columnFieldMap[key]] = dat[key];
					console.log("Excel Data", columnFieldMap[key], dat[key]);
				}
			});
			Object.keys(filDat).length > 0 && filteredData.push(filDat);
		});

		const worksheet = XLSX.utils.json_to_sheet(filteredData);

		const workbook = XLSX.utils.book_new();
		XLSX.utils.book_append_sheet(
			workbook,
			worksheet,
			parentName ? parentName : "Sheet1"
		);
		XLSX.writeFile(
			workbook,
			`${parentName ? `${parentName}_` : ""}${formatDate(new Date())}.xlsx`
		);
	}

	const handleContextMenu = (event) => {
		event.preventDefault();

		if (menu) {
			menu.style.left = `${event.pageX}px`;
			menu.style.top = `${event.pageY}px`;
			return;
		}

		const newMenu = document.createElement("div");
		newMenu.style.position = "absolute";
		newMenu.style.backgroundColor = "white";
		newMenu.style.border = "1px solid black";
		newMenu.style.borderRadius = "5px";
		newMenu.style.boxShadow = "2px 2px 5px rgba(0, 0, 0, 0.3)";
		// newMenu.style.padding = '10px'
		newMenu.style.cursor = "pointer";

		const toExcelOption = document.createElement("div");
		toExcelOption.style.display = "flex";
		toExcelOption.style.alignItems = "center";
		toExcelOption.style.padding = "5px";
		toExcelOption.style.marginBottom = "5px";

		toExcelOption.innerHTML = ReactDOMServer.renderToString(
			React.createElement(RiFileExcel2Line, {
				size: 20,
				style: { marginRight: "5px" },
			})
		);

		const text = document.createElement("span");
		text.textContent = "toExcel";
		toExcelOption.appendChild(text);
		toExcelOption.addEventListener("click", exportToExcel);
		newMenu.appendChild(toExcelOption);

		newMenu.style.left = `${event.pageX}px`;
		newMenu.style.top = `${event.pageY}px`;
		window.document.body.appendChild(newMenu);

		const closeMenu = () => {
			window.document.body.removeChild(newMenu);
			window.removeEventListener("click", closeMenu);
			setMenu(null);
		};
		window.addEventListener("click", closeMenu);

		setMenu(newMenu);
	};

	return (
		<div className="flex flex-col w-full h-full relative overflow-x-auto shadow-md sm:rounded-lg">
			{filterGlobal && (
				<GlobalFilter filter={globalFilter} setFilter={setGlobalFilter} />
			)}

			<table
				{...getTableProps()}
				className="min-w-full divide-y divide-gray-200"
			>
				<thead className="bg-gray-50">
					{headerGroups.map((headerGroup) => (
						<tr {...headerGroup.getHeaderGroupProps()}>
							{headerGroup.headers.map((column) => (
								<th
									{...column.getHeaderProps(column.getSortByToggleProps())}
									className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
									scope="col"
								>
									{column.render("Header")}
									{/*<div>{column.canFilter ? column.render('Filter'): null}</div>*/}
									<span>
										{column.isSorted ? (column.isSortedDesc ? " ▲" : " ▼") : ""}
									</span>
								</th>
							))}
						</tr>
					))}
				</thead>
				<tbody
					{...getTableBodyProps()}
					className="bg-white divide-y divide-gray-200"
					onContextMenu={handleContextMenu}
				>
					{page.map((row) => {
						prepareRow(row);
						return (
							<tr {...row.getRowProps()}>
								{row.cells.map((cell) => {
									return (
										<td
											{...cell.getCellProps()}
											scope="row"
											className="text-center px-6 py-4 whitespace-nowrap  text-sm font-medium"
										>
											{cell.render("Cell")}
										</td>
									);
								})}
							</tr>
						);
					})}
				</tbody>
			</table>
			{pagination === true &&
				<nav
					aria-label="Page navigation example"
					className="p-4 bg-white rounded-lg shadow"
				>
					<ul className="flex flex-wrap items-center  text-sm text-gray-500 gap-1">
						<li className=" hover:underline">
							Página {pageIndex + 1} de {pageOptions.length} &nbsp;
						</li>
						<li className=" hover:underline">| Ir a:&nbsp; </li>
						<li className=" hover:underline">
							<input
								className="appearance-none block w-full px-1 py-1.5 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
								type="number"
								defaultValue={pageIndex + 1}
								onChange={(e) => {
									const pageNumber = e.target.value
										? Number(e.target.value) - 1
										: 0;
									gotoPage(pageNumber);
								}}
								style={{ width: "50px" }}
							/>
						</li>
						<li className=" hover:underline">
							<button
								className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
								onClick={() => gotoPage(0)}
								disabled={!canPreviousPage}
							>
								{"<<"}
							</button>
						</li>
						{/*<Select value={pageSize} onChange={e => setPageSize(Number(e.target.value))}  options={[{value:10, label: 10},*/}
						{/*                                                                                        {value:20, label: 20},*/}
						{/*                                                                                        {value:30, label: 30}]}/>*/}
						<li className=" hover:underline">
							<button
								className="inline-flex items-center px-2 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
								onClick={() => previousPage()}
								disabled={!canPreviousPage}
								tabIndex={-1}
							>
								Anterior
							</button>
						</li>
						<li className=" hover:underline">
							<button
								className="inline-flex items-center px-2 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
								onClick={() => nextPage()}
								disabled={!canNextPage}
							>
								Siguiente
							</button>
						</li>
						<li className=" hover:underline">
							<button
								className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
								onClick={() => gotoPage(pageCount - 1)}
								disabled={!canNextPage}
							>
								{">>"}
							</button>
						</li>
					</ul>
					{/*<div>*/}
					{/*    <button onClick={exportToExcel}>Export to Excel</button>*/}
					{/*</div>*/}
				</nav>
			}

		</div>
	);
}
