import React, { useMemo } from "react";
import { useTable } from "react-table";

export function SimpleTable({ COLUMNS, data, hiddenColumns }) {
	const columns = useMemo(() => COLUMNS, []);
	const tableInstance = useTable({
		columns: columns,
		data,
		initialState: { hiddenColumns: hiddenColumns ? hiddenColumns : [] },
	});

	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		rows,
		prepareRow,
		state,
	} = tableInstance;

	const { pageIndex, pageSize } = state;

	return (
		<>
			<div className="relative overflow-x-auto shadow-md sm:rounded-lg h-full">
				<table
					{...getTableProps()}
					className="min-w-full divide-y divide-gray-200"
				>
					<thead className="bg-gray-50">
						{headerGroups.map((headerGroup) => (
							<tr {...headerGroup.getHeaderGroupProps()}>
								{headerGroup.headers.map((column) => (
									<th
										{...column.getHeaderProps()}
										scope="col"
										className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
									>
										{column.render("Header")}
									</th>
								))}
							</tr>
						))}
					</thead>

					<tbody
						{...getTableBodyProps()}
						className="bg-white divide-y divide-gray-200"
					>
						{rows.map((row, i) => {
							prepareRow(row);
							return (
								<tr {...row.getRowProps()} className="justify-between w-full">
									{row.cells.map((cell) => {
										return (
											<td
												// style={cell.show === false ? "visibility:hidden": ""}
												className="text-center px-4 py-3 whitespace-nowrap text-sm font-medium"
												scope="row"
												{...cell.getCellProps()}
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
			</div>
		</>
	);
}
