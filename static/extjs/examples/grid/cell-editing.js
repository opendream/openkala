Ext.Loader.setConfig({
    enabled: true
});
Ext.Loader.setPath('Ext.ux', '../ux');

Ext.require([
    'Ext.selection.CellModel',
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.state.*',
    'Ext.form.*',
    'Ext.ux.CheckColumn'
]);

Ext.onReady(function(){

    function formatDate(value){
        return value ? Ext.Date.dateFormat(value, 'M d, Y') : '';
    }

    Ext.define('Plant', {
        extend: 'Ext.data.Model',
        fields: [
            // the 'name' below matches the tag name to read, except 'availDate'
            // which is mapped to the tag 'availability'
            {name: 'common', type: 'string'},
            {name: 'botanical', type: 'string'},
            {name: 'light'},
            {name: 'price', type: 'float'},
            // dates can be automatically converted by specifying dateFormat
            {name: 'availDate', mapping: 'availability', type: 'date', dateFormat: 'm/d/Y'},
            {name: 'indoor', type: 'bool'}
        ]
    });


    // create the Data Store
    var store = Ext.create('Ext.data.Store', {
        // destroy the store if the grid is destroyed
        autoDestroy: true,
        model: 'Plant',
        proxy: {
            type: 'ajax',
            // load remote data using HTTP
            url: 'plants.xml',
            // specify a XmlReader (coincides with the XML format of the returned data)
            reader: {
                type: 'xml',
                // records will have a 'plant' tag
                record: 'plant'
            }
        },
        sorters: [{
            property: 'common',
            direction:'ASC'
        }]
    });

    var cellEditing = Ext.create('Ext.grid.plugin.CellEditing', {
        clicksToEdit: 1
    });

    // create the grid and specify what field you want
    // to use for the editor at each header.
    var grid = Ext.create('Ext.grid.Panel', {
        store: store,
        columns: [{
            id: 'common',
            header: 'Common Name',
            dataIndex: 'common',
            flex: 1,
            field: {
                allowBlank: false
            }
        }, {
            header: 'Light',
            dataIndex: 'light',
            width: 130,
            field: {
                xtype: 'combobox',
                typeAhead: true,
                triggerAction: 'all',
                store: [
                    ['Shade','Shade'],
                    ['Mostly Shady','Mostly Shady'],
                    ['Sun or Shade','Sun or Shade'],
                    ['Mostly Sunny','Mostly Sunny'],
                    ['Sunny','Sunny']
                ],
                lazyRender: true,
                listClass: 'x-combo-list-small'
            }
        }, {
            header: 'Price',
            dataIndex: 'price',
            width: 70,
            align: 'right',
            renderer: 'usMoney',
            field: {
                xtype: 'numberfield',
                allowBlank: false,
                minValue: 0,
                maxValue: 100000
            }
        }, {
            header: 'Available',
            dataIndex: 'availDate',
            width: 95,
            renderer: formatDate,
            field: {
                xtype: 'datefield',
                format: 'm/d/y',
                minValue: '01/01/06',
                disabledDays: [0, 6],
                disabledDaysText: 'Plants are not available on the weekends'
            }
        }, {
            xtype: 'checkcolumn',
            header: 'Indoor?',
            dataIndex: 'indoor',
            width: 55
        }],
        selModel: {
            selType: 'cellmodel'
        },
        renderTo: 'editor-grid',
        width: 600,
        height: 300,
        title: 'Edit Plants?',
        frame: true,
        tbar: [{
            text: 'Add Plant',
            handler : function(){
                // Create a record instance through the ModelManager
                var r = Ext.ModelManager.create({
                    common: 'New Plant 1',
                    light: 'Mostly Shady',
                    price: 0,
                    availDate: Ext.Date.clearTime(new Date()),
                    indoor: false
                }, 'Plant');
                store.insert(0, r);
                cellEditing.startEditByPosition({row: 0, column: 0});
            }
        }],
        plugins: [cellEditing]
    });

    // manually trigger the data store load
    store.load({
        // store loading is asynchronous, use a load listener or callback to handle results
        callback: function(){
            Ext.Msg.show({
                title: 'Store Load Callback',
                msg: 'store was loaded, data available for processing',
                modal: false,
                icon: Ext.Msg.INFO,
                buttons: Ext.Msg.OK
            });
        }
    });
});
