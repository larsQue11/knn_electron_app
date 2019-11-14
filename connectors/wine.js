function sendToPython(query) {

    // Use python shell
    let {PythonShell} = require('python-shell');

    console.log("Results in: " + query)
    
    var options = {
        mode: 'text',
        pythonPath: './venv/bin/python',
        args : query
    }

    PythonShell.run('./backend/knn_wine.py',options,function(err,results) {
        if (err) throw err;
        console.log(results)
        console.log(typeof results)
        //Do things with the returned results from knn_wine.py here:
        var tableRef = document.getElementById("table").getElementsByTagName("tbody")[0]
        var newRow = tableRef.insertRow(tableRef.rows.length)
        var i = 0
        for (x of results){
            var newCell = newRow.insertCell(i)
            var newText = document.createTextNode(x)
            newCell.appendChild(newText)
            i = i + 1
        }
    })
}

function get_data() {

    console.log("get_data/wine.js called")

    if (document.getElementById("fixed_acidity").value.length > 0) {
        var fixed_acidity = document.getElementById("fixed_acidity").value
    } else { var fixed_acidity = -1 }
    
    if (document.getElementById("volatile_acidity").value.length > 0) {
        var volatile_acidity = document.getElementById("volatile_acidity").value
    } else { var volatile_acidity = -1 }

    if (document.getElementById("citric_acid").value.length > 0) {
        var citric_acid = document.getElementById("citric_acid").value
    } else { var citric_acid = -1 }
    
    if (document.getElementById("residual_sugar").value.length > 0) {
        var residual_sugar = document.getElementById("residual_sugar").value
    } else { var residual_sugar = -1 }

    if (document.getElementById("chlorides").value.length > 0) {
        var chlorides = document.getElementById("chlorides").value
    } else { var chlorides = -1 }
    
    if (document.getElementById("free_sulfur_dioxides").value.length > 0) {
        var free_sulfur_dioxides = document.getElementById("free_sulfur_dioxides").value
    } else { var free_sulfur_dioxides = -1 }

    if (document.getElementById("total_sulfur_dioxides").value.length > 0) {
        var total_sulfur_dioxides = document.getElementById("total_sulfur_dioxides").value
    } else { var total_sulfur_dioxides = -1 }
    
    if (document.getElementById("density").value.length > 0) {
        var density = document.getElementById("density").value
    } else { var density = -1 }

    if (document.getElementById("pH").value.length > 0) {
        var pH = document.getElementById("pH").value
    } else { var pH = -1 }
    
    if (document.getElementById("sulphates").value.length > 0) {
        var sulphates = document.getElementById("sulphates").value
    } else { var sulphates = -1 }

    if (document.getElementById("alcohol").value.length > 0) {
        var alcohol = document.getElementById("alcohol").value
    } else { var alcohol = -1 }

    var k = document.getElementById("k_value").value
    var query = [k, fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
        chlorides, free_sulfur_dioxides, total_sulfur_dioxides, density, pH, sulphates, alcohol]
    console.log("Retrieved data from HTML: " + query)

    sendToPython(query)
}

function clear_data() {

    console.log('clear_data called')
    document.getElementById("fixed_acidity").value = ""
    document.getElementById("volatile_acidity").value = ""
    document.getElementById("citric_acid").value = ""
    document.getElementById("residual_sugar").value = ""
    document.getElementById("chlorides").value = ""
    document.getElementById("free_sulfur_dioxides").value = ""
    document.getElementById("total_sulfur_dioxides").value = ""
    document.getElementById("density").value = ""
    document.getElementById("pH").value = ""
    document.getElementById("sulphates").value = ""
    document.getElementById("alcohol").value = ""

    var tb = document.getElementById("table")
    for(var i = tb.rows.length - 1; i > 0; i--) {
        tb.deleteRow(i)
    }
}