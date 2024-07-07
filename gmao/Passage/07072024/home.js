$(document).ready(function () {
    let doleanceTable;
    let personnelTable;
    let portofolioTable;
    document.addEventListener('DOMContentLoaded', function () {
        const upperCaseInputs = document.querySelectorAll('input[type="text"], textarea');
        upperCaseInputs.forEach(input => {
            input.addEventListener('input', function () {
                this.value = this.value.toUpperCase();
            });
        });
    });

    function offsetAnchor() {
        if (location.hash.length !== 0) {
            window.scrollTo(window.scrollX, window.scrollY - 60);
        }
    }

    // Appliquer l'ajustement au chargement de la page
    $(window).on("hashchange", function () {
        offsetAnchor();
    });

    // Déclencher le hashchange initial
    window.setTimeout(function () {
        offsetAnchor();
    }, 1);

    function initDoleanceTable() {
        if ($('#demandeencours').length && !$.fn.DataTable.isDataTable('#demandeencours')) {
            doleanceTable = $('#demandeencours').DataTable({
                striping: false,
                'ajax': {
                    "type": "GET",
                    "url": "/home/getDoleanceEncours",
                    "dataSrc": function (json) {
                        return json;
                    }
                },
                'columns': [
                    {'data': "id"},
                    {'data': "ndi"},
                    {
                        'data': 'date_transmission',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                return moment(data).format('DD/MM/YYYY HH:mm');
                            }
                            return data;
                        }
                    },
                    {
                        'data': "statut",
                        'render': function (data, type, row) {
                            switch (data) {
                                case 'NEW':
                                    return 'NEW';
                                case 'ATT':
                                    return 'ATT';
                                case 'INT':
                                    return 'INT';
                                case 'ATP':
                                    return 'ATP';
                                case 'ATD':
                                    return 'ATD';
                                case 'TER':
                                    return 'TER';
                                default:
                                    return data;
                            }
                        }
                    },
                    {'data': "station.libelle_station"},
                    {'data': 'element'},
                    {'data': 'panne_declarer'},
                    {
                        'data': 'date_deadline',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                return moment(data).format('DD/MM/YYYY HH:mm');
                            }
                            return data;
                        }
                    },
                    {'data': 'commentaire'},
                    {
                        'data': null,
                        'render': function (data, type, row) {
                            let buttons = '';
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                buttons += '<button class="btn btn-primary btn-sm declencher-intervention" data-id="' + row.id + '">Déclencher intervention</button> ';
                            }
                            return buttons;
                        }
                    },
                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                dom: 'Bfrtip',
                buttons: [
                    {
                        extend: 'excel',
                        text: 'Exporter en Excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ],
                ordering: false,
                columnDefs: [
                    {
                        targets: '_all',
                        className: 'dt-head-nowrap',
                        render: function (data, type, row) {
                            if (type === 'display' && data != null && data.length > 70) {
                                return `<span title="${data}">${data.substr(0, 70)}...</span>`;
                            }
                            return data;
                        }
                    },
                    {
                        targets: [0],
                        visible: false,
                        searchable: false
                    },
                    {responsivePriority: 1, targets: 1}, // NDI
                    {responsivePriority: 2, targets: 3}, // Statut
                    {responsivePriority: 3, targets: 6}, // Panne déclarée
                    {responsivePriority: 10000, targets: [2, 4, 5, 7, 8]}
                ],
                createdRow: function (row, data, dataIndex) {
                    if (data.statut === 'NEW') {
                        $(row).addClass('table-success');
                    } else if (data.statut === 'ATP') {
                        $(row).addClass('table-warning');
                    } else if (data.statut === 'ATD') {
                        $(row).addClass('table-infodanger');
                    }
                },
            });
        }
    }

    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });

    function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                'ajax': {
                    "type": "GET",
                    "url": "/home/getPersonnel/",
                    "dataSrc": function (json) {
                        console.log("Données du personnel reçues:", json);
                        return json;
                    }
                },
                'columns': [
                    {'data': "id"},
                    {'data': "nom_personnel"},
                    {'data': "prenom_personnel"},
                    {
                        'data': "statut",
                        'render': function (data, type, row) {
                            let statusIcon = '';
                            let statusText = '';
                            switch (data) {
                                case 'PRS':
                                    statusIcon = '<i class="fas fa-check-circle text-success"></i>';
                                    statusText = 'Présent';
                                    break;
                                case 'ABS':
                                    statusIcon = '<i class="fas fa-times-circle text-danger"></i>';
                                    statusText = 'Absent';
                                    break;
                                case 'ATT':
                                    statusIcon = '<i class="fas fa-clock text-warning"></i>';
                                    statusText = 'Tâche attribuée';
                                    break;
                                case 'INT':
                                    statusIcon = '<i class="fas fa-hard-hat text-info"></i>';
                                    statusText = 'En intervention';
                                    break;
                            }
                            return `${statusIcon} ${statusText}`;
                        }
                    },
                    {
                        'data': null,
                        'render': function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="'
                                    + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="'
                                    + row.id + '">Marquer départ</button>';
                            } else {
                                return '';
                            }
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                ordering: false,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {
                        targets: [0],
                        visible: false,
                        searchable: false,
                    },
                    {
                        targets: [3],
                        render: function (data) {
                            return data === 'PRS' ? '<span class="badge bg-success">PRS</span>' :
                                data === 'ATT' ? '<span class="badge bg-warning">ATT</span>' :
                                    data === 'INT' ? '<span class="badge bg-info">INT</span>' :
                                        '<span class="badge bg-danger">ABS</span>';
                        }
                    },
                    {
                        targets: '_all',
                        className: 'dt-head-nowrap'
                    },
                    {responsivePriority: 1000, targets: 1}, // Nom
                    {responsivePriority: 1, targets: 2}, //
                    {responsivePriority: 2, targets: 3},
                ]
            });
        }
    }

    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        if (!$.fn.DataTable.isDataTable('#demandeencours')) {
            initDoleanceTable();
        }
        if (!$.fn.DataTable.isDataTable('#personnel')) {
            initPersonnelTable();
        }
    } else if ($('#portfolioContainer').length) {
        //loadTechnicienPortfolio();
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
        $('#demandeencours').DataTable().draw();
        $('#personnel').DataTable().draw();
    });
});