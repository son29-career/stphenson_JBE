<?php

use Illuminate\Http\Request;
use App\Models\Contact;
use Illuminate\Support\Facades\Storage;

$router->post('/upload', function (Request $request) {
    $request->validate([
        'contacts' => 'required|file|mimes:json',
    ]);

    // Store file in storage/app/contacts/
    $path = $request->file('contacts')->store('contacts');

    // Process the file in Python (assume a separate Python service handles this)
    return response()->json(['message' => 'File uploaded successfully', 'path' => $path], 200);
});

$router->get('/contacts', function (Request $request) {
    $query = Contact::query();

    if ($request->has('name')) {
        $query->where('name', 'like', '%' . $request->name . '%');
    }

    if ($request->has('email')) {
        $query->where('email', 'like', '%' . $request->email . '%');
    }

    $contacts = $query->paginate(10);

    return response()->json($contacts, 200);
});

$router->get('/contacts/{id}', function ($id) {
    $contact = Contact::findOrFail($id);
    return response()->json($contact, 200);
});

$router->put('/contacts/{id}', function (Request $request, $id) {
    $contact = Contact::findOrFail($id);
    $contact->update($request->only('name', 'email', 'phone'));

    return response()->json(['message' => 'Contact updated successfully'], 200);
});

$router->delete('/contacts/{id}', function ($id) {
    $contact = Contact::findOrFail($id);
    $contact->delete();

    return response()->json(['message' => 'Contact deleted successfully'], 200);
});

