/*!
* Aloha Editor
* Author & Copyright (c) 2010 Gentics Software GmbH
* aloha-sales@gentics.com
* Licensed unter the terms of http://www.aloha-editor.com/license.html
*/
(function(window, undefined) {
  var 
    jQuery = window.alohaQuery, $ = jQuery,
    GENTICS = window.GENTICS,
    Aloha = window.Aloha;


  /**
   * register the plugin with unique name
   */
  Aloha.Undo = new Aloha.Plugin('undo');

  /**
   * Configure the available languages
   */
  Aloha.Undo.languages = ['en', 'de'];

  /**
   * Initialize the plugin and set initialize flag on true
   */
  Aloha.Undo.init = function () {
      
      stack = new Undo.Stack();

      var EditCommand = Undo.Command.extend({
        constructor: function(editable, oldValue, newValue) {
          this.editable = editable;
          this.oldValue = oldValue;
          this.newValue = newValue? newValue: editable.getContents();
        },
        execute: function() {
        },
        undo: function() {
          this.reset(this.oldValue);
        },

        redo: function() {
          this.reset(this.newValue);
        },
        reset: function(val) {
          if (this.editable.isActive) {
            this.editable.blur();
          }
          this.editable.obj.html(val);
          this.editable.activate();
          // restore selection
        }
      });

      stack.changed = function(command) {
        // update UI
      };

      $(document).keydown(function(event) {
        if (!event.metaKey || (event.keyCode != 90 && event.keyCode != 57)) {
          return;
        }
        event.preventDefault();
        if (event.shiftKey) {
          stack.canRedo() && stack.redo();
        } else {
          stack.canUndo() && stack.undo();
        }
      });


      Aloha.bind('aloha-editable-activated', function (jevent, aevent) {
        aevent.editable.undoContent = aevent.editable.getContents();
      });

      Aloha.bind('aloha-smart-content-changed', function (jevent, aevent) {
          // workaround because on redo the editable must be blured.
          if (  aevent.triggerType == 'spec' && 
                aevent.editable && 
                aevent.editable.undoContent != aevent.editable.getContents() && 
                aevent.editable.keyCode != 90) {
                  var undoContent = aevent.editable.undoContent;
                  stack.execute( new EditCommand( aevent.editable, undoContent) );
                  aevent.editable.undoContent = aevent.editable.getContents()
                  aevent.editable.setUnmodified();
          }
          else if ( aevent.triggerType == 'blur' || aevent.triggerType == 'idle') {
            Aloha.trigger('aloha-smart-content-changed',{
              'editable' : aevent.editable,
              'keyIdentifier' : null,
              'keyCode' : null,
              'char' : null,
              'triggerType' : 'spec',
              'snapshotContent' : aevent.snapshotContent
            });
          }
      });
  };

  /**
  * toString method
  * @return string
  */
  Aloha.Undo.toString = function () {
    return 'undo';
  };

}) (window);
