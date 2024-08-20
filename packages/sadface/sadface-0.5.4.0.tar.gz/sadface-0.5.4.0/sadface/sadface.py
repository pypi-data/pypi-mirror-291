#!/usr/bin/python

import argparse
import cmd
import codecs
import datetime
import json
import sys
import textwrap
import uuid

from . import config
from . import validation
from . import version

sd = {}

def add_support(con_text=None, prem_text=None, con_id=None, prem_id=None):
    """
    Syntactic sugar to create an argument structure from a set of texts.
    Given a conclusion text & a list of premise texts. Creates an intermediate,
    default "support" scheme.

    This makes it easier to build a SADFace document without manually creating
    and organising individual nodes.

    Returns an argument dict, e.g.

    {
        "conclusion": atom,
        "scheme": atom,
        "premises": [atom(s)]
    }

    Returns: a dict
    """
    if((con_text is not None or con_id is not None) and (prem_text is not None or prem_id is not None)):

        if con_text is not None:
            c = add_atom(con_text)
        else:
            c = get_atom(con_id)

        s = add_inference("support")
        try:
            add_edge(s["id"], c["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        p_list = []
        if(prem_text is not None):
            for text in prem_text:
                atom = add_atom(text)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")
        if(prem_id is not None):
            for atom_id in prem_id:
                atom = get_atom(atom_id)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")

        arg = {"conclusion":c, "scheme":s, "premises":p_list}
        return arg
    return None


def add_edge(source_id, target_id):
    """
    Given a source atom ID & a target atom ID, create an 
    edge linking the two and add it to the sadface doc,
    "sd" & return the dict representing the edge. If
    either of source or target IDs is invalid then an
    exception is raised.

    Returns: a dict 
    """
    if ((get_node(source_id) is not None) and (get_node(target_id) is not None)):
        edge = new_edge(source_id, target_id)
        sd["edges"].append(edge)
        return edge
    raise Exception("Could not create new edge between: "+source_id+" & "+target_id)

def add_atom(text):
    """
    Create a new argument atom using the supplied text

    Returns: the new atom dict
    """
    atomid = contains_atom(text)
    atom = None

    if atomid is not None:
        atom = get_atom(atomid)

    else:
        atom = new_atom(text)
        sd["nodes"].append(atom)
    
    return atom

def add_atom_metadata(atom_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair, to the atom dict identified
    by the supplied atom ID and metadata namespace.

    Note that "core" should be reserved for sadface default metadata only

    Additional namespaces can be any string but should normally follow
    the reversed domain name approach to provide some level of uniqueness
    and avoid unnecessary clashes
    """
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                if node["metadata"].get(namespace) is None:
                    node["metadata"][namespace] = {}
                    node["metadata"][namespace][key] = value
                else:
                    node["metadata"][namespace][key] = value

def add_conflict(name):
    """
    Add a new conflict node dict to the sadface document. The conflict type
    is identified by the supplied name

    Returns: The new conflict dict
    """
    conflict = new_conflict(name)
    sd["nodes"].append(conflict)
    return conflict

def add_conflict_metadata(conflict_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair, to the conflict dict identified
    by the supplied conflict ID and metadata namespace.

    Note that "core" is reserved for sadface default metadata only

    Additional namespaces can be any string but should normally follow
    the reversed domain name approach to provide some level of uniqueness
    and avoid unnecessary clashes
    """
    for node in sd["nodes"]:
        if "conflict" == node["type"]:
            if conflict_id == node["id"]:
                if node["metadata"].get(namespace) is None:
                    node["metadata"][namespace] = {}
                    node["metadata"][namespace][key] = value
                else:
                    node["metadata"][namespace][key] = value

def add_global_metadata(namespace, key, value):
    """
    Add metadata, a key:value pair to the base sadface doc
    """
    if sd["metadata"].get(namespace) is None:
        sd["metadata"][namespace] = {}
        sd["metadata"][namespace][key] = value
    else:
        sd["metadata"][namespace][key] = value

def add_notes(text):
    """
    Add a metadata entry for the document that contains notes. Notes
    are miscellaneous, unstructured free text.
    """
    sd["metadata"]["core"]["notes"] = text


def add_resource(content):
    """
    Create a new resource dict using the supplied content string
    then add to the resourses list of the sadface doc

    Returns: the new resource dict
    """
    res = new_resource(content)
    sd["resources"].append(res)
    return res

def add_resource_metadata(resource_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair to the resource dict identified
    by the supplied atom ID.    
    """
    for res in sd["resources"]:
        if res["id"] == resource_id:
            if res["metadata"].get(namespace) is None:
                res["metadata"][namespace] = {}
                res["metadata"][namespace][key] = value
            else:
                res["metadata"][namespace][key] = value

def add_inference(name):
    """
    Add a new inference node dict to the sadface document. The scheme type
    associated with the inference is identified by the supplied name

    Returns: The new inference dict
    """
    inference = new_inference(name)
    sd["nodes"].append(inference)
    return inference

def add_inference_metadata(inference_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair, to the inference dict identified
    by the supplied inference ID and metadata namespace.

    Note that "core" is reserved for sadface default metadata only.

    Additional namespaces can be any string but should normally follow
    the reversed domain name approach to provide some level of uniqueness
    and avoid unnecessary clashes.
    """
    for node in sd["nodes"]:
        if "inference" == node["type"]:
            if inference_id == node["id"]:
                if node["metadata"].get(namespace) is None:
                    node["metadata"][namespace] = {}
                    node["metadata"][namespace][key] = value
                else:
                    node["metadata"][namespace][key] = value


def add_source(atom_id, resource_id, text, offset, length):
    """
    Add a new source dict to the atom identified by the supplied
    atom ID. The new source refers to the an existing resource that
    is identified by the supplied resource ID. The source identifies
    text string in the resource dict that it references as well as
    the offset & length of the text from the beginning of the resource

    Returns: The new source dict
    """
    source = new_source(resource_id, text, offset)
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["sources"].append(source)
                return source

def append_notes(text):
    """
    Append new text to an existing notes entry
    """
    if sd.get("metadata").get("core").get("notes") != None:
        sd["metadata"]["core"]["notes"] += text
    else:
        add_notes(text)

def build_argument(con_text=None, prem_text=None, con_id=None, prem_id=None):
    """
    Syntactic sugar to create an argument structure from a set of texts.
    Given a conclusion text & a list of premise texts. Creates an intermediate,
    default, "inference" node named "support".

    This makes it easier to build a SADFace document without manually creating
    and organising individual nodes.

    Returns an argument dict, e.g.

    {
        "conclusion": atom,
        "inference": atom,
        "premises": [atom ID(s)]
    }

    e.g.

    {
        "conclusion": {
            "id": "329aee40-b34d-4eaa-9e25-9ef3098b4cfa",
            "type": "atom",
            "text": "You should treasure every moment",
            "sources": [],
            "metadata": {
                "core": {}
            }
        },
        "inference": {
            "id": "f4ae4161-f18b-49f7-9213-d81c2084cedd",
            "type": "inference",
            "name": "support",
            "metadata": {
                "core": {}
            }
        },
        "premises": ["6b4cbe35-4e11-4126-ab25-97c9ac651647", "4cebed0d-3869-4a20-958c-9e164a019573"]
    }

    Returns: a dict
    """
    if((con_text is not None or con_id is not None) and (prem_text is not None or prem_id is not None)):

        if con_text is not None:
            c = add_atom(con_text)
        else:
            c = get_atom(con_id)

        i = add_inference("support")
        try:
            add_edge(i["id"], c["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        p_list = []
        if(prem_text is not None):
            for text in prem_text:
                atom = add_atom(text)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], i["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")
        if(prem_id is not None):
            for atom_id in prem_id:
                atom = get_atom(atom_id)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], i["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")

        arg = {"conclusion":c, "inference":i, "premises":p_list}
        return arg
    return None

def build_attack(attacker_text=None, target_text=None, attacker_id=None, target_id=None):
    """
    SADFace primarily support two forms of conflict, Disagreement and attack (We consider defeat
    to be a specific interpretation derived from the extistence of an attack relationship so do
    not explicity represent it at present. Defeat might be better represented as a status, perhaps 
    transient, that is either derived at runtime from the state of the graph or else is stored 
    more permanently within the metadata for a given attack). 

    A single attack node is used to point, via edge nodes from one atom node, the source of the 
    attack, to another atom node, the destination of the attack. Attack is a binary relationship 
    that has exactly two forms within SADFace:

    -- An argument may attack itself, i.e. the source and destination ends of the attack relate
    to the same atom.
    -- An argument may attack another argument, i.e. the source and destination are different
    atoms.

    We depict attack through the use of a node that represent the attack relationship. This
    function will instantiate a conflict node between two nodes (either pre-existing & identifed by 
    node IDs or created by this function from supplied texts, or a mixture of the two).

    Returns a conflict dict, e.g.

    {
        "attacker": atom,
        "conflict": atom,
        "target": atom
    }
    (where the scheme just happens to depict a conflict)

    
    For example:

    {
        "attacker": {
            "id": "6399c86d-3c07-4223-ae91-bb989b6dc21e",
            "type": "atom",
            "text": "You are going to die",
            "sources": [],
            "metadata": {
                "core": {}
            }
        },
        "conflict": {
            "id": "7b4b7d23-7386-470e-ad48-56a655812218",
            "type": "conflict",
            "name": "attack",
            "metadata": {
                "core": {}
            }
        },
        "target": {
            "id": "777a21cf-6c60-44cc-9b3f-bfe1f2e342d6",
            "type": "atom",
            "text": "I might live forever",
            "sources": [],
            "metadata": {
                "core": {}
            }
        }
    }

    Returns: a dict
    """
    if((attacker_text is not None or attacker_id is not None) and (target_text is not None or target_id is not None)):
        
        if attacker_text is not None:
            a = add_atom(attacker_text)
        else:
            a = get_atom(attacker_id)

        c = add_conflict("attack")

        try:
            add_edge(c["id"], a["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        if target_text is not None:
            d = add_atom(target_text)
        else:
            d = get_atom(target_id)

        try:
            add_edge(d["id"], c["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        arg = {"attacker":a, "conflict":c, "target":d}
        return arg
    return None


def build_disagreement(arg_text=None, disagreement_text=None, arg_id=None, disagreement_id=None):
    """
    SADFace primarily support two forms of conflict, Disagreement and attack (We consider defeat
    to be a specific interpretation derived from the extistence of an attack relationship so do
    not explicity represent it at present). Disagreements create a relationship between two or 
    more arguments to indicate that the arguments mutually disagree with each other.

    A single disagreement node is used to point, via edge nodes to the collection of arguments
    that disagree with each other. A disagreement must link at least two different argument nodes,
    identifed by different node IDs, in order to create the relationship between them.


    We depict conflict through the use of a node that represent the conflict relationship. This
    function will instantiate a conflict node between two nodes (either pre-existing & identifed by 
    node IDs or created by this function from supplied texts, or a mixture of the two).

    Returns a conflict dict, e.g.

    {
        "argument_1": atom,
        "conflict": atom,
        "argument_2": atom
    }
    (where the scheme just happens to depict a conflict)

    
    For example:

    {
        "argument_1": {
            "id": "6399c86d-3c07-4223-ae91-bb989b6dc21e",
            "type": "atom",
            "text": "You are going to die",
            "sources": [],
            "metadata": {
                "core": {}
            }
        },
        "conflict": {
            "id": "7b4b7d23-7386-470e-ad48-56a655812218",
            "type": "conflict",
            "name": "disagreement",
            "metadata": {
                "core": {}
            }
        },
        "argument_2": {
            "id": "777a21cf-6c60-44cc-9b3f-bfe1f2e342d6",
            "type": "atom",
            "text": "I might live forever",
            "sources": [],
            "metadata": {
                "core": {}
            }
        }
    }

    Returns: a dict
    """
    if((arg_text is not None or arg_id is not None) and (disagreement_text is not None or disagreement_id is not None)):
        
        if arg_text is not None:
            a = add_atom(arg_text)
        else:
            a = get_atom(arg_id)

        c = add_conflict("disagree")

        try:
            add_edge(c["id"], a["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        if disagreement_text is not None:
            d = add_atom(disagreement_text)
        else:
            d = get_atom(disagreement_id)

        try:
            add_edge(c["id"], d["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        arg = {"argument_1":a, "conflict":c, "argument_2":d}
        return arg
    return None


def clear_notes():
    """
    Remove any existing notes
    """
    sd.get("metadata").get("core").pop("notes")


def contains_atom(atom_text):
    """
    Searches the sadface document for an existing atom containing
    the supplied text. If found, returns the id of that atom,
    otherwise None
    """
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_text == node["text"]:
                return node["id"]
    return None

def delete_atom(atom_id):
    """
    Remove the atom from the sadface document identified by the
    supplied atom ID
    """
    atom = get_atom(atom_id)
    sd["nodes"].remove(atom)

    conns = get_connections(atom_id)
    for c in conns:
        delete_edge(c["id"])

def delete_conflict(conflict_id):
    """
    Remove the conflict from the sadface document identified by the
    supplied conflict ID

    """
    conflict = get_conflict(conflict_id)
    sd["nodes"].remove(conflict)

    conns = get_connections(conflict_id)
    for c in conns:
        delete_edge(c["id"])

def delete_edge(edge_id):
    """
    Remove the edge from the sadface document identified by the
    supplied edge ID

    """
    edge = get_edge(edge_id)
    sd["edges"].remove(edge)

def delete_source(atom_id, resource_id):
    """
    Remove a source from the atom identified by the
    supplied atom ID & resource ID respectively

    """
    source = get_source(atom_id, resource_id)
    if source is not None:
        atom = get_atom(atom_id)
        atom["sources"].remove(source)

def delete_resource(resource_id):
    """
    Remove the resource from the sadface document identified by the
    supplied resource ID

    """
    resource = get_resource(resource_id)
    sd["resources"].remove(resource)

def delete_inference(inference_id):
    """
    Remove the inference from the sadface document identified by the
    supplied inference ID

    """
    inference = get_inference(inference_id)
    sd["nodes"].remove(inference)

    conns = get_connections(inference_id)
    for c in conns:
        delete_edge(c["id"])

def export_cytoscape():
    """
    Cytoscape.js is a useful graph visualisation library for Javascript. However
    it uses some slightly different keynames and includes description of visual
    elements, useful to Cytoscape's visualisation, but having no place in SADFace.

    Both nodes & edges in a Cytoscape graph are collated together into a single
    eleents object so we need to do that to the SADFace nodea & edges. Furthemore,
    each node and edge object must contain a data object. After that conversion is
    a relatively straightforward mapping:

    EDGES
        id -> id
        source_id -> source
        target_id -> target

        e.g. 
        {
            "data": {
                "source": "a1",
                "id": "a1s1",
                "target": "s1"
            }
        }

    NODES - ATOMS    
        id -> id
        type -> type
        text -> content
        + "classes":"atom-label"
        + "typeshape":"roundrectangle"

        e.g.
        {
            "classes": "atom-label",
            "data": {
                "content": "Every person is going to die",
                "type": "atom",
                "id": "a1",
                "typeshape": "roundrectangle"
            }
        }


    NODES - SCHEMES
        id -> id
        type -> type
        name -> content
        + "classes":"scheme-label"
        + "typeshape":"diamond"
        
        e.g.
        {
            "classes": "scheme-label",
            "data": {
                "content": "Default\nSupport",
                "type": "scheme",
                "id": "s1",
                "typeshape": "diamond"
            }
        }

    """
    cy = {}
    cy['elements'] = {}
    cy['elements']['nodes'] = []
    cy['elements']['edges'] = []

    for edge in sd['edges']:
        e = {}
        e['data'] = {}
        e['data']['id'] = edge['id']
        e['data']['source'] = edge['source_id']
        e['data']['target'] = edge['target_id']

        cy['elements']['edges'].append(e)

    for node in sd['nodes']:
        n = {}
        n['data'] = {}
        n['data']['id'] = node['id']
        n['data']['type'] = node['type']
        if n['data']['type'] == "atom":
            n['classes'] = "atom-label"
            n['data']['typeshape'] = "roundrectangle"
            n['data']['content'] = node['text']

        else:
            n['classes'] = "scheme-label"
            n['data']['typeshape'] = "diamond"
            n['data']['content'] = node['name']

        cy['elements']['nodes'].append(n)

    return  json.dumps(cy)

def export_dot(trad=True):
    """
    Exports a subset of SADFace to the DOT graph description language

    Returns: String-encoded DOT document
    """
    if trad:
        colour_scheme = "X11"
        support_colour = "darkolivegreen3"
        disagree_colour = "firebrick2"
        default_colour = "cornsilk4"
    else:
        colour_scheme = "ylgnbu3"
        support_colour = "1"
        disagree_colour = "3"
        default_colour = "2"

    max_length = 25
    edge_str = " -> "
    dot = "digraph SADFace {"
    dot += "node [style=\"filled\"]"
    for node in sd["nodes"]:
        if "text" in node:
            txt = node["text"]
            if len(txt) > max_length:
                txt = "\\n".join(textwrap.wrap(txt, max_length))
            line = '"{}"'.format(node['id']) + " [label=\"" + txt + "\"]" + " [shape=box, style=rounded];\n"
            dot += line
        elif "name" in node:
            if "support" == node.get("name"):
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+support_colour\
                + ", shape=diamond];\n"
            elif "disagree" == node.get("name"):
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+disagree_colour\
                + ", shape=diamond];\n"
            elif "attack" == node.get("name"):
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+disagree_colour\
                + ", shape=diamond];\n"
            else:
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+default_colour\
                + ", shape=diamond];\n"

            dot += line

    for edge in sd["edges"]:
        source = get_node(edge["source_id"])
        target = get_node(edge["target_id"])
        
        if("atom" == source["type"]):
            dot += '"{}"'.format(source["id"])
        elif "inference" == source["type"]:
            dot += '"{}"'.format(source["id"])
        elif "conflict" == source["type"]:
            dot += '"{}"'.format(source["id"])
        
        dot += edge_str

        if("atom" == target["type"]):
            dot += '"{}"'.format(target["id"])
        elif "inference" == target["type"]:
            dot += '"{}"'.format(target["id"])
        elif "conflict" == target["type"]:
            dot += '"{}"'.format(target["id"])

        
        dot += ";\n"

    dot += "}"
    
    return dot

def export_json():
    """
    Dump the current sadface document to a JSON string

    Returns: String-encoded JSON
    """
    return json.dumps(sd)

def get_analyst():
    """
    Retrieve the name of the argument analyst in the SADFace doc
    """
    return sd["metadata"]["core"]["analyst_name"]

def get_atom(atom_id):
    """
    Retrieve the atom dict identified by the supplied atom ID

    Returns: An atom dict
    """
    for node in sd["nodes"]:
        if atom_id == node["id"]:
            return node

def get_atom_id(text):
    """
    Retrieve the first atom whose text equals the supplied text

    Returns: The atom's ID or None 
    """
    for node in sd["nodes"]:
        if text == node.get("text"):
            return node["id"]

def get_atom_metadata(atom_id, namespace=None, key=None):
    """
    Retrieve an atom's metadata. Results depend upon the specificity of the request
    which must include atom_id.

    If atom_id only is provided then all metadata assocaited with the atom is returned
    If atom_id + namespace is provided then only the specified namespace is returned
    If atom_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    atom = get_atom(atom_id)
    if atom is not None:
        if namespace is None:
            return atom.get("metadata")
        else:
            if key is None:
                return atom.get("metadata").get(namespace)
            else:
                return atom.get("metadata").get(namespace).get(key)


def get_atom_text(atom_id):
    """
    Retrieve the atom dict identified by the supplied atom ID

    Returns: An atom dict
    """
    for node in sd["nodes"]:
        if atom_id == node["id"]:
            return node["text"]

def get_claim():
    """
    Retrieve the claim metadata entry from the document
    """
    return sd["metadata"].get("core").get("claim")

def get_conflict(conflict_id):
    """
    Retrieve the conflit dict identified by the supplied conflict ID

    Returns: A conflict dict
    """
    for node in sd["nodes"]:
        if conflict_id == node["id"]:
            return node

def get_conflict_metadata(conflict_id, namespace=None, key=None):
    """
    Retrieve a conflict's metadata. Results depend upon the specificity of the request
    which must include a valid conflict_id.

    If conflict_id only is provided then all metadata associated with the conflict is returned
    If conflict_id + namespace is provided then only the specified namespace is returned
    If conflict_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict or None
    """
    conflict = get_conflict(conflict_id)
    if conflict is not None:
        if namespace is None:
            return conflict.get("metadata")
        else:
            if key is None:
                return conflict.get("metadata").get(namespace)
            else:
                return conflict.get("metadata").get(namespace).get(key)


def get_connections(node_id):
    """
    Given a node id, retrieve a list containing all edges that connnect it
    to other nodes
    """
    conn =  []
    for edge in sd["edges"]:
        if node_id == edge["source_id"] or node_id == edge["target_id"]:
            conn.append(edge)
    return conn

def get_created():
    """
    Retrieve the claim metadata entry from the document
    """
    return sd["metadata"].get("core").get("created")

def get_document():
    """
    Retrieve the current SADFace document
    """
    return sd

def get_document_id(doc = None):
    """
    Retrieve the SADFace document's ID
    """
    if doc is None:
        return sd["metadata"].get("core").get("id")
    else:
        return doc["metadata"].get("core").get("id")

def get_description():
    """
    Retrieve the description metadata entry from the document
    """
    return sd["metadata"].get("core").get("description")

def get_edited():
    """
    Retrieve the last edited timestamp from the sadface document
    """
    return sd["metadata"].get("core").get("edited")

def get_edge(edge_id):
    """
    Retrieve the edge dict identified by the supplied edge ID

    Returns: An edge dict
    """
    for edge in sd["edges"]:
        if edge_id == edge["id"]:
            return edge

def get_global_metadata(namespace=None, key=None):
    """
    Retrieve the document's metadata. Results depend upon the specificity of the request
    which must include atom_id.

    If neither namespace nor key are provided then all metadata associated with the document is returned
    If a namespace is provided then only the specified namespace is returned
    If a namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    if namespace is None:
        return sd.get("metadata")
    else:
        if key is None:
            return sd.get("metadata").get(namespace)
        else:
            return sd.get("metadata").get(namespace).get(key)



def get_node(node_id):
    """
    Given a node's ID but no indication of node type, return the node if 
    it exists or else indicate that it doesn't to the caller.

    Returns: A node dict or None
    """
    for node in sd["nodes"]:
        if node_id == node["id"]:
            return node

def get_notes():
    """
    Retrieve the notes metadata entry from the document
    """
    return sd["metadata"].get("core").get("notes")

def get_resource(resource_id):
    """
    Retrieve the resource dict identified by the supplied resource ID

    Returns: An resource dict
    """
    for resource in sd["resources"]:
        if resource_id == resource["id"]:
            return resource

def get_resource_metadata(resource_id, namespace=None, key=None):
    """
    Retrieve a resource's metadata. Results depend upon the specificity of the request
    which must include a resource_id.

    If resource_id only is provided then all metadata assocaited with the resource is returned
    If reource_id + namespace is provided then only the specified namespace is returned
    If resource_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    resource = get_resource(resource_id)
    if resource is not None:
        if namespace is None:
            return resource.get("metadata")
        else:
            if key is None:
                return resource.get("metadata").get(namespace)
            else:
                return resource.get("metadata").get(namespace).get(key)

def get_inference(inference_id):
    """
    Retrieve the inference dict identified by the supplied inference ID

    Returns: An inference dict if found otherwise None
    """
    for node in sd["nodes"]:
        if inference_id == node["id"]:
            return node

def get_inference_metadata(inference_id, namespace=None, key=None):
    """
    Retrieve an inference's metadata. Results depend upon the specificity of the request
    which must include a valid inference_id.

    If inference_id only is provided then all metadata associated with the scheme is returned
    If inference_id + namespace is provided then only the specified namespace is returned
    If inference_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict or None
    """
    inference = get_inference(inference_id)
    if inference is not None:
        if namespace is None:
            return inference.get("metadata")
        else:
            if key is None:
                return inference.get("metadata").get(namespace)
            else:
                return inference.get("metadata").get(namespace).get(key)

def get_source(atom_id, resource_id):
    """
    Retrieve the source dict identified by the supplied source ID

    Returns: An source dict
    """
    atom = get_atom(atom_id)
    if atom is not None:
        if len(atom["sources"]) > 0:
            for source in atom["sources"]:
                if resource_id == source["resource_id"]:
                    return source
            
def get_title():
    """
    Retrieve the title metadata entry from the document
    """
    return sd["metadata"].get("core").get("title")

def get_version():
    """
    Return a string indicating the version of the loaded SADFace document
    If no version parameter then version is less than <0.1
    Versioning introduced in v0.2 with introduction of version key to
        {"metadata":{ "core": { "version": "0.1"} }, ...}
    """
    version = sd.get("metadata").get("core").get("version")
    if None == version:
        print("no explicit version so 0.1")
        version = "0.1"

    return version


def import_json(json_string):
    """
    Take a string-encoded JSON document and loads it into a Python dict

    Returns: the loaded dict
    """
    return json.loads(json_string)

def initialise():
    """
    Reads the config file from the supplied location then uses the data
    contained therein to personalise a new SADFace document

    Returns: A Python dict representing the new SADFace document
    """
    global sd
    sd = new_sadface()
    return sd#new_sadface()

def list_atoms():
    """
    Return a list of atoms and their associated ID contained in the current 
    document, using the following format

    [ { 'id':'id-value', 'text':'text-value' } ]

    """
    atoms = []
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            tmp = {}
            tmp["id"] = node["id"]
            tmp["text"] = node["text"]
            atoms.append(tmp)
    return atoms

def list_arguments():
    """
    Use to retrieve a list of arguments in the current document. Minimally
    we expect that each argument contains at least one sceheme node, so, by
    extension, a list of scheme nodes is also a list of arguments

    Returns: A list of scheme IDs
    """
    schemes = []
    for node in sd["nodes"]:
        if "scheme" == node["type"]:
            schemes.append(node.get("id"))
    return schemes

def list_conflict():
    """
    Use to retrieve a list of conflict nodes from the current document.

    Returns: A list of conflict IDs
    """
    conflicts = []
    for node in sd["nodes"]:
        if "conflict" == node["type"]:
            conflicts.append(node.get("id"))
    return conflicts

def list_resources():
    """
    Returns a comma separated list of resource IDs
    """
    return [ res["id"] for res in sd["resources"] ]

def list_inferences():
    """
    Use to retrieve a list of inference nodes from the current document.

    Returns: A list of inference IDs
    """
    inferences = []
    for node in sd["nodes"]:
        if "inference" == node["type"]:
            inferences.append(node.get("id"))
    return inferences


def load_from_file(filename):
    """
    Load the sadface document stored in the file identifed by the supplied
    filename.
    """
    try:
        with open(filename) as sadface_file:
            return json.load(sadface_file)
    except IOError:
        print("Could not read file:", filename)


def new_atom(text):
    """
    Creates a new SADFace atom node (Python dict) using the supplied text

    Returns: A Python dict representing the new SADFace atom
    """
    new_atom = {"id":new_uuid(), "type":"atom", "text":text, "sources":[], "metadata":{"core": {}}}
    return new_atom

def new_conflict(name):
    """
    Create a new SADFace conflict (Python dict) using the supplied conflict name. The conflict
    name should refer to a known conflict type from the set of {disagree | attack | defeat}

    Returns: A Python dict representing the new SADFace conflict
    """
    new_conflict = {"id":new_uuid(), "type":"conflict", "name":name, "metadata":{ "core": {}}}
    return new_conflict

def new_edge(source_id, target_id):
    """
    Creates & returns a new edge dict using the supplied source & 
    target IDs

    Returns: A Python dict representing the new edge
    """
    new_edge = {"id":new_uuid(), "source_id":source_id, "target_id":target_id}
    return new_edge

def new_sadface():
    """
    Creates & returns a new SADFace document

    Returns: A Python dict representing the new SADFace document
    """
    if config.location is None:
        new_doc = {"metadata":{ "core":{"version":version.__version__, "id":new_uuid(), "analyst_name":"A User", "analyst_email":"user@email.address", "created":now(), "edited":now()}}, "resources":[], "nodes":[], "edges":[]}

    else:
        new_doc = {"metadata":{ "core":{"version":version.__version__, "id":new_uuid(), "analyst_name":config.current.get("analyst", "name"), "analyst_email":config.current.get("analyst", "email"), "created":now(), "edited":now()}}, "resources":[], "nodes":[], "edges":[]}
    return new_doc

def new_resource(content):
    """
    Given the supplied content (Python String), create a new resource dict

    The arguments that SADFace describes are either constructed directly in a tool that writes
    them to this format, or else are sourced from elsewhere, e.g. an argumentative text or
    webpage, or else perhaps another medium, such as audio or video. Currently SADFace supports
    textual resources which are stored in the content key. Optionally a 
        "url":"some web location"
    pair can be added to the metadata to indicate a specific web location. Alternatively:
        "doi":"digital object identifier" - resolvable by dx.doi.org
        "magnet-link":"a torrent file"
        "isbn":"for books"
    Metadata may also store additional bibliographic or referencing/citation information
    as defined in bibtex formats.

    Returns: A Python dict representing the new SADFace resource
    """
    new_resource = {"id":new_uuid(), "content":content, "type":"text", "metadata":{ "core": {}}}
    return new_resource

def new_inference(name):
    """
    Create a new SADFace inference (Python dict) using the supplied scheme name. The scheme
    name should ideally refer to an existing scheme from a known schemeset

    Returns: A Python dict representing the instantiation of new SADFace inference
    """
    new_inference = {"id":new_uuid(), "type":"inference", "name":name, "metadata":{ "core": {}}}
    return new_inference

def new_source(resource_id, text, offset):
    """
    Create a new SADFace source (Python dict) using the supplied resource ID (a source always
    refers to an existing resource object) and identifying a section of text in the resource 
    as well as an offset for locating the text in the original resource.

    Text segment length is calculated from the length of the supplied text.

    As the resource object is enhanced to account for newer "types" of resource, so the
    source object must be enhanced to keep track and enable sources to index sub-parts of
    resources.

    Returns: A Python dict representing the new SADFace source
    """
    length = len(text)
    new_source = {"resource_id":resource_id, "text":text, "offset":offset, "length":length}
    return new_source

def new_uuid():
    """
    Utility method to generate a new universally unique ID. Used througout to uniquely
    identify various items such as atoms, schemes, resources, & edges

    Returns: A string
    """
    return str(uuid.uuid4())

def now():
    """
    Utility method to produce timestamps in ISO format without the microsecond
    portion, e.g. 2017-07-05T17:21:11

    Returns: A String
    """
    return datetime.datetime.now().replace(microsecond=0).isoformat()

def prettyprint(doc=None):
    """
    Retrieve a nicely formatted string encoded version of the SADFace document

    Returns: A String
    """
    string = sd
    if(doc is not None):
        string = doc
    return json.dumps(string, indent=4, sort_keys=True)

def print_doc(doc=None):
    """
    Retrieve a string encoded version of the SADFace document

    Returns: A String
    """
    string = sd
    if(doc is not None):
        string = doc
    return json.dumps(string,sort_keys=True)

def reset():
    """
    Return SADFace to it's initial state

    Basically delete, remove, or nullify any settings that have been applied.
    """
    global sd
    sd = {}
    config.reset()

def save(filename=None, filetype="json"):
    """
    Write the prettyprinted SADFace document to a file on disk.

    The default filetype is JSON. Other supported export formats are: 
    - Cytoscape
    - GraphViz/Dot
    
    """
    f = filename
    d = None
    pathname = None

    if filename is None:       
        if config.current is not None:
            f = config.current.get("file","name")
            d = config.current.get("file","dir")
            outname = f+d
        else:
            f = "out"
            d = ""
            pathname = f
    else:
        pathname = f


    if ("dot" == filetype):
        suffix = '.dot'
        if not pathname.endswith(suffix):
            pathname += suffix

        with codecs.open(pathname, 'w', 'utf-8') as outfile:
            outfile.write(export_dot())

    elif("cytoscape" == filetype):
        suffix = '.json'
        if not pathname.endswith(suffix):
            pathname += suffix
        
        with codecs.open(pathname, 'w', 'utf-8') as outfile:
            outfile.write(prettyprint(json.loads(export_cytoscape())))
    else:
        suffix = '.json'
        if not pathname.endswith(suffix):
            pathname += suffix
        
        with open(pathname, 'w') as outfile:
            json.dump(sd, outfile, indent=4, sort_keys=True, ensure_ascii=False)

def set_analyst(analyst):
    """
    sets the name of the argument analyst in the SADFace doc to the supplied name
    """
    sd["metadata"]["core"]["analyst_name"] = analyst
    
def set_atom_text(atom_id, new_text):
    """
    An atoms text key:value pair is the canonical representation of a portion of text 
    that exists in an argument. This should be updatable so that the overall document 
    makes sense. Links to original source texts are maintained via the source list 
    which indexes original text portions of linked resources.

    Returns: The updated atom dict
    """
    atom = get_atom(atom_id)
    if(atom is not None):
        atom["text"] = new_text
        return atom
    else:
        raise Exception("Could not set the text value for atom: "+atom_id)

def set_doc(newdoc):
    """
    Replaces the existing SADFace document with the supplied $newdoc
    """
    global sd
    sd = newdoc

def set_title(text):
    """
    Set a metadata entry for the document that contains a title. This is a
    useful but non-essential addendum to the base sadface document when
    building systems that make use of sadface.
    """
    sd["metadata"]["core"]["title"] = text

def set_claim(atom_id):
    """
    Enables a given atom to be nominated as the claim for the argument captured
    by this sadface document. A useful way to explicitly set the atom that should
    be considered to be the main claim.
    """
    atom = get_atom(atom_id)
    if(atom is not None): 
        sd["metadata"]["core"]["claim"] = atom_id
    else:
        raise Exception("Can't make atom ("+atom_id+") a claim because it doesn't exist")

def set_conflict_name(conflict_id, conflict_name):
    """
    Given an ID for an existing conflict node, set the name associated with it and return the 
    updated conflict node.
    
    Returns: Updated conflict dict
    """
    conflict = get_conflict(conflict_id)
    if(conflict is not None):
        conflict["name"] = conflict_name
        return conflict
    else:
        raise Exception("Could not set the name of conflict: "+conflict_id)

def set_created(timestamp):
    """
    Sets the creation timestamp for the SADFace document to the supplied timestamp.
    This can be useful when moving analysed argument data between formats whilst
    maintaining original metadata.
    """
    sd["metadata"]["core"]["created"] = timestamp

def set_description(text):
    """
    Set a metadata entry for the document that contains a description.
    """
    sd["metadata"]["core"]["description"] = text

def set_edited(timestamp):
    """
    Set the last edited timestamp for the SADFace doc to match the supplied
    timestamp. This can be useful when moving analysed argument data between formats 
    whilst maintaining original metadata.
    """
    sd["metadata"]["core"]["edited"] = timestamp

def set_document_id(id):
    """
    Set the SADFace document ID to match the supplied ID. This can be useful when 
    moving analysed argument data between formats whilst maintaining original metadata.
    """
    sd["metadata"]["core"]["id"] = id

def set_inference_name(inference_id, scheme_name):
    """
    Given an ID for an existing inference node, set the scheme name associated with it 
    and return the inference node.
    
    Returns: Updated inference dict
    """
    inference = get_inference(inference_id)
    if(inference is not None):
        inference["name"] = scheme_name
        return inference
    else:
        raise Exception("Could not set the name of inference: "+inference_id)

def update():
    """
    Updates the last edited timestamp for the SADFace doc to now
    """
    sd["metadata"]["core"]["edited"] = now()

