{% if not invEvent %}
    function updateMiscCost(itemID, rowID, colID, newValue, oldValue) {
        var jsonDict = new Object();
        jsonDict.miscCostID = itemID.slice(0, -4);
        var costName = 0,
            costAmount = 1;

        switch(colID) {
            case costName:
                jsonDict.name = newValue;
                $.ajax({
                    url: "/api/miscCost/setName",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(jsonDict),
                    async: false,
                    error: function(response) {
                        alert("Could not set miscellaneous costs! \n Error - " + JSON.parse(response.responseText).error);
                        costGrid.setValueAt(rowID, colID, oldValue, true);
                    },
                });
                break;
            case costAmount:
                jsonDict.amount = newValue;
                $.ajax({
                    url: "/api/miscCost/setAmount",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(jsonDict),
                    async: false,
                    error: function(response) {
                        alert("Could not set miscellaneous costs! \n Error - " + JSON.parse(response.responseText).error);
                        costGrid.setValueAt(rowID, colID, oldValue, true);
                    },
                });
                break;
        }
    }

    function addMiscCost() {
        if ($("#mcAmountField").val() && $("#mcNameField").val()) {
            var jsonDict = new Object();
            jsonDict.eventID = "{{event.ID}}";
            jsonDict.name = $("#mcNameField").val();
            jsonDict.amount = $("#mcAmountField").val();

            $.ajax({
                url: "/api/miscCost/newMiscCost",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                success: function(response) {
                    costGrid.append(response.miscCostID + "cost", {"cost name": jsonDict.name, "amount": jsonDict.amount}, true);
                    costGrid.refreshGrid();
                },
                error: function(response) {
                    alert("Could not set miscellaneous costs! \n Error - " + JSON.parse(response.responseText).error);
                },
            });
        } else {
            alert("Please fill in all necessary information.");
        }
    }

    function deleteMiscCost(costID) {
        var jsonDict = new Object;
        console.log("costID: " + costID);
        jsonDict.miscCostID = costID.slice(0, -4);
        console.log("actual ID " + jsonDict.miscCostID);
        $.ajax({
            url: "/api/miscCost/deleteMiscCost",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonDict),
            success: function(response) {
                var rowIndex = costGrid.getRowIndex(costID);
                costGrid.remove(rowIndex);
            },
            error: function(response) {
                alert("Could not remove cost! \n Error - " + response.responseText);
            },
        });
    }

    function copyInventory() {
        $("#copyInventoryButton").attr("disabled", true);
        var jsonDict = new Object();
        jsonDict.eventID = {{event.ID}};
        $.ajax({
            url: "/api/event/copyInventory",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonDict),
            success: function(response) {
                location.reload();
            },
            error: function(response) {
                alert("Could not copy inventory! \n Error - " + JSON.parse(response.responseText).error);
            },
        });
    }
{% endif %}

function roundDecimal(num) {
    return Math.round(num*100)/100;
}

function makeEditableGrid() {
    editableGrid = new EditableGrid("InventoryEditableGrid", 
        { sortIconUp: "/static/images/up.png", 
        sortIconDown: "/static/images/down.png",
        modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) { updateItem(row.id, rowIdx, colIdx, newValue, oldValue); }});

    editableGrid.load({ metadata: [
        { name: "name", datatype: "string", editable: true },
        { name: "fandom", datatype: "string", editable: true },
        { name: "kind", datatype: "string", editable: true },
        { name: "price", datatype: "double($,2,dot,comma,1)", editable: true },
        { name: "cost", datatype: "double($,2,dot,comma,1)", editable: true },
        { name: "remaining", datatype: "integer(,-1,dot,comma,1)", editable: true },
        {% if not invEvent %}
            { name: "sold", datatype: "integer(,-1,dot,comma,1)", editable: true },
        {% endif %}
        { name: "action", datatype: "html", editable: false }
    ]});

    editableGrid.setCellRenderer("action", new CellRenderer({render: function(cell, value) {
        var rowID = editableGrid.getRowId(cell.rowIndex);
        cell.innerHTML = '<a onclick="duplicateItem(' + rowID + ')" style="cursor:pointer"><i class="fa fa-clone"></i></a>';
        cell.innerHTML += '&nbsp;<a onclick="deleteItem(' + rowID + ')" style="cursor:pointer"><i class="fa fa-trash"></i></a>';
    }})); 

    editableGrid.attachToHTMLTable("inventory");
    editableGrid.renderGrid();

    {% if not invEvent %}
        costGrid = new EditableGrid("CostEditableGrid",
            { sortIconUp: "/static/images/up.png", 
            sortIconDown: "/static/images/down.png",
            modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) { updateMiscCost(row.id, rowIdx, colIdx, newValue, oldValue); }});

        costGrid.load({ metadata: [
            { name: "cost name", datatype: "string", editable: true },
            { name: "amount", datatype: "double($,2,dot,comma,1)", editable: true },
            { name: "action", datatype: "html", editable: false }
        ]});

        costGrid.setCellRenderer("action", new CellRenderer({render: function(cell, value) {
            var rowID = costGrid.getRowId(cell.rowIndex);
            //cell.innerHTML = '<a onclick="deleteMiscCost()" style="cursor:pointer"><i class="fa fa-trash"></i></a>';
            cell.innerHTML = '<a onclick="deleteMiscCost(\'' + rowID.toString() + '\')" style="cursor:pointer"><i class="fa fa-trash"></i></a>';
        }}));

        costGrid.attachToHTMLTable("cost-chart");
        costGrid.renderGrid();
    {% endif %}
}

function appendAutoComplete() {
    fandomResults = [
        {% for fandom in fandoms %}
            "{{fandom}}",
        {% endfor %}
    ];

    $("#new-fandom").autocomplete({
        source: fandomResults,
        open: function(){
            $(".ui-autocomplete").append('<li class="ui-menu-item" data-toggle="modal" data-target="#fandomModal" aria-label="Add New">+ New Fandom</li>');
        },
        response: function(event, ui) {
            if (ui.content.length === 0) {
                $("#add-new-fandom").removeClass("hidden");
            } else {
                $("#add-new-fandom").addClass("hidden");
            }
        }
    });

    kindResults = [
        {% for kind in kinds %}
            "{{kind}}",
        {% endfor %}
    ];

    $("#new-kind").autocomplete({
        source: kindResults,
        open: function(){
            $(".ui-autocomplete").append('<li class="ui-menu-item" data-toggle="modal" data-target="#kindModal" aria-label="Add New">+ New Kind</li>');
        },
        response: function(event, ui) {
            if (ui.content.length === 0) {
                $("#add-new-kind").removeClass("hidden");
            } else {
                $("#add-new-kind").addClass("hidden");
            }
        }
    });
}

$(function() {
    // add editable grid
    makeEditableGrid();
    // make new fandom and new kinds in add new form searchable
    appendAutoComplete();
    $('[data-toggle="tooltip"]').tooltip();
});

function makeNewItem() {
    makeItem($("#new-name").val(), 
             "{{event.ID}}", 
             $("#new-fandom").val(), 
             $("#new-kind").val(), 
             roundDecimal($("#new-price").val()), 
             roundDecimal($("#new-cost").val()), 
             $("#new-numLeft").val(), 
             {% if invEvent %}
                0);
             {% else %}
                $("#new-numSold").val());
             {% endif %}
}

function duplicateItem(rowID) {
    var rowIndex = editableGrid.getRowIndex(rowID);
    makeItem(editableGrid.getValueAt(rowIndex, 0),
            "{{event.ID}}", 
            editableGrid.getValueAt(rowIndex, 1), 
            editableGrid.getValueAt(rowIndex, 2), 
            editableGrid.getValueAt(rowIndex, 3), 
            editableGrid.getValueAt(rowIndex, 4), 
            editableGrid.getValueAt(rowIndex, 5), 
            {% if invEvent %}
                0);
            {% else %}
               editableGrid.getValueAt(rowIndex, 6));
            {% endif %}
}

function makeItem(itemName, eventID, itemFandom, itemKind, itemPrice, itemCost, itemNumLeft, itemNumSold) {

    var jsonDict = new Object();
    jsonDict.name = itemName;
    jsonDict.eventID = eventID;
    jsonDict.fandom = itemFandom;
    jsonDict.kind = itemKind;
    jsonDict.price = itemPrice;
    jsonDict.cost = itemCost;
    jsonDict.numLeft = itemNumLeft;
    jsonDict.numSold = itemNumSold;

    $.ajax({
        url: "/api/item/newItem",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(jsonDict),
        success: function(response) {
            editableGrid.append(response.itemID, {"name": itemName, "fandom": itemFandom, "kind": itemKind, "price": itemPrice, "cost": itemCost, "remaining": itemNumLeft{% if not invEvent %}, "sold": itemNumSold{% endif %}}, true);
            editableGrid.refreshGrid();
        },
        error: function(response) {
            alert('Error: \n' + JSON.parse(response.responseText).error);
        },
    });
}

function updateItem(itemID, rowID, colID, newValue, oldValue) {
    var name = 0,
        fandom = 1,
        kind = 2,
        price = 3,
        cost = 4,
        numLeft = 5
        {% if not invEvent %}
            , numSold = 6
        {% endif %};

    var jsonDict = new Object();
    jsonDict.itemID = itemID;

    switch(colID) {
        case name:
            jsonDict.name = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setName",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new name! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        case fandom:
            jsonDict.fandom = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setFandom",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new fandom! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        case kind:
            jsonDict.kind = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setKind",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new kind! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        case price:
            jsonDict.price = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setPrice",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new price! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        case cost:
            jsonDict.cost = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setCost",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new cost! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        case numLeft:
            jsonDict.numLeft = newValue;
            var ajaxObj = $.ajax({
                url: "/api/item/setNumLeft",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(jsonDict),
                error: function(response) {
                    alert("Could not set new number remaining! \n Error - " + JSON.parse(response.responseText).error);
                    editableGrid.setValueAt(rowID, colID, oldValue, true);
                },
            });
            break;
        {% if not invEvent %}
            case numSold:
                jsonDict.numSold = newValue;
                var ajaxObj = $.ajax({
                    url: "/api/item/setNumSold",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(jsonDict),
                    error: function(response) {
                        alert("Could not set new number sold! \n Error - " + JSON.parse(response.responseText).error);
                        editableGrid.setValueAt(rowID, colID, oldValue, true);
                    },
                });
                break;
        {% endif %}
    }
}

function deleteItem(itemID) {
    if (confirm("Are you sure you want to delete this?")) {
        var jsonDict = new Object();
        jsonDict.itemID = itemID;
        var ajaxObj = $.ajax({
            url: "/api/item/deleteItem",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonDict),
            success: function(response) {
                //$("#" + itemID + "nameField").closest("tr").remove();
                var rowIndex = editableGrid.getRowIndex(itemID);
                editableGrid.remove(rowIndex);
                //editableGrid.remove();
                // Editable Grid shuffles everything inside the tr but not the tr itself... so the IDs don't match up
            },
            error: function(response) {
                alert("Could not delete item! \n Error - " + JSON.parse(response.responseText).error);
            },
        });
    }
}

function toggleItemForm() {
    {% if invEvent %}
        var buttonStr = "#new-numLeft";
    {% else %}
        var buttonStr = "#new-numSold";
    {% endif %}
    if ($("#item-form").css("display") == "none") {
        $("#item-form").show("slow", function() {});
        var KEYUP = function(event) {
            if (event.keyCode == 13) {
                $("#add-item").click();
            }
        }
        $(buttonStr).keyup(KEYUP);
    } else {
        $("#item-form").hide("slow", function() {});
        $(buttonStr).unbind("keyup", KEYUP);
    }
}

function makeFandom() {
    var jsonDict = new Object();
    jsonDict.name = $("#fandomField").val();
    console.log(jsonDict.name);
    $.ajax({
        url: "/api/fandom/newFandom",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(jsonDict),
        success: function(response) {
            fandomResults.push(jsonDict.name);
            $("#fandomModal").modal("hide");
            $("#new-fandom").val(jsonDict.name);
            $("#add-new-fandom").addClass("hidden");
        },
        error: function(response) {
            alert("Could not make new fandom! \n Error - " + JSON.parse(response.responseText).error);
        },
    });
}

function makeKind() {
    var jsonDict = new Object();
    jsonDict.name = $("#kindField").val();
    console.log(jsonDict.name);
    $.ajax({
        url: "/api/kind/newKind",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(jsonDict),
        success: function(response) {
            kindResults.push(jsonDict.name);
            $("#kindModal").modal("hide");
            $("#new-kind").val(jsonDict.name);
            $("#add-new-kind").addClass("hidden");
        },
        error: function(response) {
            alert("Could not set new kind! \n Error - " + JSON.parse(response.responseText).error);
        },
    });
}