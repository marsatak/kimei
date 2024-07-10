function initPortfolioTable(data, interventionEnCoursGlobal) {
    console.log("Initialisation de la table avec les données:", data);
    if ($('#portfolioTable').length) {
        if ($.fn.DataTable.isDataTable('#portfolioTable')) {
            $('#portfolioTable').DataTable().destroy();
        }

        try {
            $('#portfolioTable').DataTable({
                data: data,
                columns: [
                    // ... vos colonnes existantes ...
                ],
                responsive: {
                    details: {
                        type: 'column',
                        target: 'tr',
                        renderer: function (api, rowIdx, columns) {
                            var data = $.map(columns, function (col, i) {
                                return col.hidden ?
                                    '<tr data-dt-row="' + col.rowIndex + '" data-dt-column="' + col.columnIndex + '">' +
                                    '<td>' + col.title + ':' + '</td> ' +
                                    '<td>' + col.data + '</td>' +
                                    '</tr>' :
                                    '';
                            }).join('');
                            return data ?
                                $('<table/>').append(data) :
                                false;
                        }
                    }
                },
                autoWidth: false,
                ordering: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                pageLength: -1,  // Affiche toutes les entrées
                lengthChange: false,  // Supprime le sélecteur de nombre d'entrées
                drawCallback: function (settings) {
                    console.log("DrawCallback - Intervention en cours (global):", interventionEnCoursGlobal);
                    $('.prendre-en-charge').prop('disabled', interventionEnCoursGlobal);
                },
                columnDefs: [
                    {
                        targets: 0,
                        className: 'control',
                        orderable: false,
                        render: function () {
                            return '<i class="fa fa-plus-square" aria-hidden="true"></i>';
                        }
                    },
                    // ... vos autres columnDefs ...
                ]
            });
        } catch (error) {
            console.error("Erreur lors de l'initialisation de la table:", error);
        }
    } else {
        console.error("L'élément #portfolioTable n'existe pas dans le DOM");
    }
}