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

      Aloha.bind('aloha-smart-content-changed', function (jevent, aevent) {
          // workaround because on redo the editable must be blured.
          if (  aevent.triggerType != 'blur' && 
                aevent.editable && 
                aevent.editable.keyCode != 90 &&
                aevent.editable.originalContent != aevent.editable.getContents()) {

                  stack.execute( new EditCommand( aevent.editable, aevent.editable.originalContent) );
                  aevent.editable.setUnmodified();
          }
          else if ( aevent.triggerType == 'blur') {
            Aloha.trigger('aloha-smart-content-changed',{
              'editable' : aevent.editable,
              'keyIdentifier' : null,
              'keyCode' : null,
              'char' : null,
              'triggerType' : 'idle',
              'snapshotContent' : aevent.editable.getSnapshotContent()
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
