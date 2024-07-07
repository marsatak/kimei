$(document).ready(function () {
    let doleanceTable, personnelTable, portofolioTable;

    function initDoleanceTable() {
        if ($('#demandeencours').length && !$.fn.DataTable.isDataTable('#demandeencours')) {
            doleanceTable = $('#demandeencours').DataTable({
                ajax: {
                    url: "/home/getDoleanceEncours",
                    dataSrc: ""
                },
                columns: [
                    {data: "ndi", width: "5%%"},
                    {
                        data: "date_transmission", width: "10%",
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: "statut", width: "5%"},
                    {data: "station.libelle_station", width: "15%"},
                    {data: 'element', width: "15%"},
                    {data: 'panne_declarer', width: "30%"},
                    {
                        data: 'date_deadline', width: "10%",
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: 'commentaire', width: "15%"},
                    {
                        data: null, width: "15%",
                        render: function (data, type, row) {
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                return '<button class="btn btn-primary btn-sm declencher-intervention" data-id="' + row.id + '">' +
                                    '<i class="fas fa-plus">@</i>' +
                                    '</button>';
                            }
                            return '';
                        }
                    },
                ],
                responsive: true,
                autoWidth: false,
                ordering: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                createdRow: function (row, data, dataIndex) {
                    $(row).addClass('status-' + data.statut)
                },
                columnDefs: [
                    {targets: [1, 6], className: 'date-column'},
                    {targets: [2], className: 'status-column'},
                    {
                        targets: '_all', render: function (data, type, row) {
                            if (type === 'display' && data != null && data.length > 70) {
                                return `<span title="${data}">${data.substr(0, 70)}...</span>`;
                            }
                            return data;
                        }
                    }
                ]
            });
        }
    }

    /*function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                ajax: {
                    url: "/home/getPersonnel/",
                    dataSrc: ""
                },
                columns: [
                    {data: "nom_personnel"},
                    {data: "prenom_personnel"},
                    {
                        data: "statut",
                        render: function (data) {
                            let statusClass = data === 'PRS' ? 'bg-success' :
                                data === 'ATT' ? 'bg-warning' :
                                    data === 'INT' ? 'bg-info' : 'bg-danger';
                            return `<span class="badge ${statusClass}">${data}</span>`;
                        }
                    },
                    {
                        data: null,
                        render: function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="' + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="' + row.id + '">Marquer départ</button>';
                            }
                            return '';
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                ordering: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {targets: [2], className: 'status-column'}
                ]
            });
        }
    }*/

    function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                ajax: {
                    url: "/home/getPersonnel/",
                    dataSrc: ""
                },
                columns: [
                    {data: "nom_personnel"},
                    {data: "prenom_personnel"},
                    {
                        data: "statut",
                        render: function (data, type, row) {
                            const statusClasses = {
                                'PRS': 'bg-success',
                                'ATT': 'bg-warning',
                                'INT': 'bg-info',
                                'ABS': 'bg-danger'
                            };
                            return `<span class="badge ${statusClasses[data] || 'bg-secondary'}">${data}</span>`;
                        },
                        className: 'status-column'
                    },
                    {
                        data: null,
                        render: function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="' + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="' + row.id + '">Marquer départ</button>';
                            }
                            return '';
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                ordering: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                }
            });
        }
    }

    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        initDoleanceTable();
        initPersonnelTable();
    } else if ($('#portfolioContainer').length) {
        loadTechnicienPortfolio();
    }

    function refreshDoleanceTable() {
        if (doleanceTable) {
            doleanceTable.ajax.reload(null, false);
        }
    }

    function refreshPersonnelTable() {
        if (personnelTable) {
            personnelTable.ajax.reload(null, false);
        }
    }

    $(window).resize(function () {
        if (doleanceTable) doleanceTable.columns.adjust().draw();
        if (personnelTable) personnelTable.columns.adjust().draw();
    });

    // Ajoutez ici les autres fonctions et gestionnaires d'événements nécessaires
});