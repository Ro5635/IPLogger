$( document ).ready(function() {



    //Configure the general model for the newServer task
    $('#launchNewServerModal').click(function(){

        //Set the modal title
        $('#generalModel .generalModalTitle').html('New Remote');

        //place the structure
        $('#generalModel .modal-body').html('<p>Enter the name for the new remote:</p><br><input type="text" class="form-control" id="newName" placeholder="New Remote Name"><br>');

        //Place the buttons:
        $('#generalModel .additionalModalButtons').html('<button id="newServer" type="button" class="btn btn-primary">Request</button>');

    });

    //The user has requested a new remote, Request a new remote from the server
    $('#generalModel').on('click', '#newServer', function(){
        //Get the users desired name
        var newName = $('#newName').val();

        //Send Post request for access details for this new remote
        $.ajax({
			url: "/newserver",
			type: "POST",
            dataType: 'json',
            contentType : 'application/json',
			data: JSON.stringify({'remote_name':  newName }),
			cache: false,
			success: function(returnedData) {
                //Update the view with the new data

                var jsonData = JSON.parse(returnedData);

                //Set the modal title
                $('#generalModel .generalModalTitle').html('New Remote');

                //Place the new structure
                $('#generalModel .modal-body').html('<p>Generated Details For ' + jsonData['remote_name'] + ' </p><br><div class="form-group row"><label for="idDisplayForm" class="col-sm-2 form-control-label">ID:</label><div class="col-sm-10"><input type="text" class="form-control" id="idDisplayForm" placeholder="loading" readonly></div></div><div class="form-group row"><label for="privKeyDisplayForm" class="col-sm-2 form-control-label">Private Key:</label><div class="col-sm-10"><input type="text" class="form-control" id="privKeyDisplayForm" placeholder="loading" readonly></div></div><br><p>Place the above details into the updater application on the remote.</p>');

                //Add the new data
                $('#idDisplayForm').val(jsonData['remote_id']);
                $('#privKeyDisplayForm').val(jsonData['new_priv_key']);

                //Clear un-required buttons
                $('#generalModel .additionalModalButtons').html('');

			}
		});

    });

});