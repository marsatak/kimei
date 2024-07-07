function chargerDetailsPieces(doleanceId) {
    // Afficher une modal ou un formulaire pour sélectionner les pièces
    // Exemple simplifié :
    let pieceId = prompt("Entrez l'ID de la pièce à affecter:");
    let quantite = prompt("Entrez la quantité:");

    if (pieceId && quantite) {
        $.ajax({
            url: AFFECTER_PIECE_URL.replace('0', equipeSelectionneeId).replace('0', doleanceId),
            method: 'POST',
            data: {
                piece_id: pieceId,
                quantite: quantite,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (response) {
                if (response.success) {
                    alert('Pièce affectée avec succès');
                    chargerDetailsEquipe(equipeSelectionneeId);
                } else {
                    alert('Erreur lors de l\'affectation de la pièce');
                }
            },
            error: function () {
                alert('Erreur lors de la communication avec le serveur');
            }
        });
    }
}

// Modifiez la fonction afficherDetailsEquipe pour inclure les pièces
function afficherDetailsEquipe(data) {
    // ... (code existant)

    let listeDoléances = $('#listeDoléances');
    listeDoléances.empty();
    data.doleances.forEach(function (doleance) {
        let doleanceItem = $('<li class="list-group-item">');
        doleanceItem.append($('<span>').text(`${doleance.ndi} - ${doleance.panne_declarer}`));

        let piecesBtn = $('<button class="btn btn-sm btn-info ml-2">').text('Pièces');
        piecesBtn.on('click', function () {
            chargerDetailsPieces(doleance.id);
        });
        doleanceItem.append(piecesBtn);

        let piecesList = $('<ul class="list-group mt-2">');
        doleance.pieces.forEach(function (piece) {
            piecesList.append($('<li class="list-group-item">').text(`${piece.libelle} - Quantité: ${piece.quantite}`));
        });
        doleanceItem.append(piecesList);

        listeDoléances.append(doleanceItem);
    });

    // ... (reste du code existant)
}