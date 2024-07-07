function chargerPiecesNonAttribuees() {
    $.get(GET_PIECES_NON_ATTRIBUEES_URL, function (data) {
        let listePiecesNonAttribuees = $('#listePiecesNonAttribuées');
        listePiecesNonAttribuees.empty();
        data.pieces.forEach(function (piece) {
            let pieceItem = $('<li class="list-group-item">');
            pieceItem.append($('<span>').text(`${piece.piece_libelle} - ${piece.piece_reference}`));
            let attribuerBtn = $('<button class="btn btn-sm btn-success">').text('Attribuer');
            attribuerBtn.on('click', function () {
                attribuerPiece(piece.id);
            });
            pieceItem.append(attribuerBtn);
            listePiecesNonAttribuees.append(pieceItem);
        });
    });
}

function attribuerPiece(pieceId) {
    let doleanceId = prompt("Entrez l'ID de la doléance à laquelle attribuer cette pièce:");
    let quantite = prompt("Entrez la quantité:");
    if (doleanceId && quantite) {
        $.post(ATTRIBUER_PIECE_URL.replace('0', equipeSelectionneeId), {
            piece_id: pieceId,
            doleance_id: doleanceId,
            quantite: quantite,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }, function (response) {
            if (response.success) {
                alert('Pièce attribuée avec succès');
                chargerDetailsEquipe(equipeSelectionneeId);
                chargerPiecesNonAttribuees();
            } else {
                alert('Erreur lors de l\'attribution de la pièce: ' + response.error);
            }
        });
    }
}

function retirerPiece(pieceId, doleanceId) {
    if (confirm('Êtes-vous sûr de vouloir retirer cette pièce ?')) {
        $.post(RETIRER_PIECE_URL.replace('0', equipeSelectionneeId), {
            piece_id: pieceId,
            doleance_id: doleanceId,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }, function (response) {
            if (response.success) {
                alert('Pièce retirée avec succès');
                chargerDetailsEquipe(equipeSelectionneeId);
                chargerPiecesNonAttribuees();
            } else {
                alert('Erreur lors du retrait de la pièce: ' + response.error);
            }
        });
    }
}

// Modifiez la fonction afficherDetailsEquipe pour inclure les pièces
function afficherDetailsEquipe(data) {
    // ... (code existant)

    let listePieces = $('#listePieces');
    listePieces.empty();
    data.doleances.forEach(function (doleance) {
        doleance.pieces.forEach(function (piece) {
            let pieceItem = $('<li class="list-group-item">');
            pieceItem.append($('<span>').text(`${piece.libelle} - Quantité: ${piece.quantite} (Doléance: ${doleance.ndi})`));
            let retirerBtn = $('<button class="btn btn-sm btn-danger">').text('Retirer');
            retirerBtn.on('click', function () {
                retirerPiece(piece.id, doleance.id);
            });
            pieceItem.append(retirerBtn);
            listePieces.append(pieceItem);
        });
    });

    chargerPiecesNonAttribuees();
}

// Ajoutez ceci à votre fonction $(document).ready()
