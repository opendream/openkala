/*
repositories = {
    CoreStandard: new GENTICS.Aloha.Repository('CoreStandard')
}

repositories.CoreStandard.query = function(p, callback) {
    var d = this.settings.data.filter(function (e, i) {
        var r = new RegExp(p.queryString, 'i');
        var ret = false;

        return (
            jQuery.inArray(e.type, p.objectTypeFilter) > -1 &&
              ( e.name.match(r) )
        )
    });
    callback.call(this, d);
}
repositories.CoreStandard.markObject = function(obj, resourceItem) {
    CoreStandard.updateCoreStandard(obj, resourceItem);
}
*/

CoreStandard = new GENTICS.Aloha.Plugin('CoreStandard');
CoreStandard.init = function() {
    var that = this;
    var insertButton = new GENTICS.Aloha.ui.Button({
        'iconClass': 'button_core_standard',
        'size': 'small',
        'onclick': function() {
            that.insertCoreStandard();
        },
        'tooltip': 'มาตรฐาน',
        'toggle': false
    });
    GENTICS.Aloha.FloatingMenu.addButton(
        'GENTICS.Aloha.continuoustext',
        insertButton,
        'มาตรฐาน',
        1
    );

    GENTICS.Aloha.FloatingMenu.createScope(this.getUID('coreStandard'), 'GENTICS.Aloha.global');
    this.coreStandardField = new GENTICS.Aloha.ui.AttributeField();
    this.coreStandardField.setTemplate('<span>{name}<br class="clear" /></span>');
    this.coreStandardField.setObjectTypeFilter(['standard']);
    this.coreStandardField.setDisplayField('name');
    GENTICS.Aloha.FloatingMenu.addButton(
        this.getUID('coreStandard'),
        this.coreStandardField,
        'มาตรฐาน'
    )
    this.coreStandardField.getExtConfigProperties = function() {
        return {
            alohaButton: this,
            xtype : 'alohaattributefield',
            rowspan: this.rowspan||undefined,
            width: this.width||undefined,
            id : this.id,
            minChars: 1
        };
    }

    GENTICS.Aloha.EventRegistry.subscribe(GENTICS.Aloha, 'selectionChanged', function(event, rangeObject) {
        var foundMarkup = that.findTag( rangeObject );
        jQuery('.core-standard-selected').removeClass('core-standard-selected');
        
        if ( foundMarkup.length != 0 ) {
            GENTICS.Aloha.FloatingMenu.setScope(that.getUID('coreStandard'));
            that.coreStandardField.setTargetObject(foundMarkup, 'data-core-standard-name');
            
            foundMarkup.addClass('core-standard-selected');
        }
        // re-layout the Floating Menu
        GENTICS.Aloha.FloatingMenu.doLayout();
    });

    GENTICS.Aloha.EventRegistry.subscribe(
        GENTICS.Aloha, 
        "editableDeactivated", 
        function (jEvent, aEvent) {
              jQuery('.core-standard-selected').removeClass('core-standard-selected');
        }
    );

};

CoreStandard.findTag = function(range) {
    return jQuery(range.commonAncestorContainer).closest('.GENTICS_block.core-standard');
};

CoreStandard.insertCoreStandard = function() {
    GENTICS.Aloha.FloatingMenu.userActivatedTab = ('มาตรฐาน');
    var range = GENTICS.Aloha.Selection.getRangeObject();
    var tpl = jQuery('<span class="GENTICS_block core-standard" contentEditable="false">' +
      '<span class="name">CODE</span></span>');
    
    GENTICS.Utils.Dom.insertIntoDOM(tpl, range, jQuery(GENTICS.Aloha.activeEditable.obj));
    range.startContainer = range.endContainer = tpl.contents().get(0);
    range.select();
    this.coreStandardField.focus();
}

CoreStandard.updateCoreStandard = function(obj, resourceItem) {
    obj.find('.name').text(resourceItem.name);
}
