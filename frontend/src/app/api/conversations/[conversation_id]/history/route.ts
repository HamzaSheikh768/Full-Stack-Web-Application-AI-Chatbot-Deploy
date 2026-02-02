import { NextRequest, NextResponse } from "next/server";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ conversation_id: string }> }
) {
  try {
    const { conversation_id } = await params;

    // Forward the request to the backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const res = await fetch(`${backendUrl}/api/conversations/${conversation_id}/history`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": req.headers.get("authorization") || "", // Pass through authorization header
      },
    });

    const data = await res.json();

    // Return the response from the backend with the same status
    return NextResponse.json(data, { status: res.status });
  } catch (error: any) {
    console.error("Conversation history proxy error:", error);

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