// Start Closure
(function(window, undefined) {
	"use strict";
	
	// Prepare
	var
		jQuery = window.alohaQuery, $ = jQuery,
		Ext = window.Ext,
		GENTICS = window.GENTICS,
		Aloha = window.Aloha;


/*!
 * This file is part of Aloha Editor
 * Author & Copyright (c) 2010 Gentics Software GmbH, aloha@gentics.com
 * Licensed unter the terms of http://www.aloha-editor.com/license.html
 */
Ext.tree.AlohaTreeLoader = function(config) {
	Ext.apply(this, config);
	Ext.tree.AlohaTreeLoader.superclass.constructor.call(this);
};

Ext.extend( Ext.tree.AlohaTreeLoader, Ext.tree.TreeLoader, {
	paramOrder: ['node', 'id'],
	nodeParameter: 'id',
	directFn : function(node, id, callback) {
		var
			params = {
				inFolderId: node.id,
				objectTypeFilter: this.objectTypeFilter,
				repositoryId: node.repositoryId
			};

		Aloha.RepositoryManager.getChildren ( params, function( items ) {
			var response = {};

			response = {
				status: true,
				scope: this,
				argument: {callback: callback, node: node}
			};

			if(typeof callback === 'function'){
				callback(items, response);
			}
		});
	},
	createNode: function(node) {
		if ( node.name ) {
			node.text = node.name;
		}
		if ( node.hasMoreItems ) {
			node.leaf = !node.hasMoreItems;
		}
		if ( node.objectType ) {
			node.cls = node.objectType;
		}
        return Ext.tree.TreeLoader.prototype.createNode.call(this, node);
    },
	objectTypeFilter : null,
	setObjectTypeFilter : function (otFilter) {
		this.objectTypeFilter = otFilter;
	},
	getObjectTypeFilter : function () {
		return this.objectTypeFilter;
	}
});

})(window);
