import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // Extract user ID from the authorization header
    const authHeader = req.headers.get("authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json(
        { error: "Authorization header required with Bearer token" },
        { status: 401 }
      );
    }

    // Decode the JWT token to extract the user ID (sub field)
    const token = authHeader.substring(7); // Remove "Bearer " prefix
    let userId = null;

    try {
      // Decode the JWT token to get the user ID from the 'sub' claim
      const tokenParts = token.split('.');
      if (tokenParts.length === 3) {
        const payload = tokenParts[1];
        // Replace URL-safe base64 characters with standard base64
        let base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
        // Add padding if needed
        const pad = base64.length % 4;
        if (pad) {
          if (pad === 1) throw new Error('Invalid token');
          base64 = base64 + '='.repeat(5 - pad);
        }
        // Decode the base64 string to JSON
        const decodedPayload = Buffer.from(base64, 'base64').toString('utf-8');
        const payloadObj = JSON.parse(decodedPayload);
        userId = payloadObj.sub;
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      return NextResponse.json(
        { error: "Invalid token format" },
        { status: 401 }
      );
    }

    if (!userId) {
      return NextResponse.json(
        { error: "User ID not found in token" },
        { status: 401 }
      );
    }

    // Forward the request to the backend with user ID in the path
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const res = await fetch(`${backendUrl}/api/${userId}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": req.headers.get("authorization") || "", // Pass through authorization header
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    // Return the response from the backend with the same status
    return NextResponse.json(data, { status: res.status });
  } catch (error: any) {
    console.error("Chat proxy error:", error);

    // Handle different types of errors appropriately
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return NextResponse.json(
        { error: "Unable to connect to chat service. Please check if the backend is running." },
        { status: 503 }
      );
    }

    return NextResponse.json(
      { error: error.message || "Failed to connect to chat service" },
      { status: 503 }
    );
  }
}