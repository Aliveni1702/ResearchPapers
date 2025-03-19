# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .fetcher import fetch_and_filter_papers
# from .serializers import papers_to_csv

# class PubMedFetchView(APIView):
#     def get(self, request):
#         query = request.query_params.get('query', None)
#         if not query:
#             return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch papers using your logic
#         papers = fetch_and_filter_papers(query)
#         if not papers:
#             return Response({"detail": "No papers found."}, status=status.HTTP_404_NOT_FOUND)

#         # Convert papers to CSV
#         csv_data = papers_to_csv(papers)

#         # Prepare the response with correct CSV headers
#         response = Response(csv_data, content_type="text/csv")
#         response['Content-Disposition'] = 'attachment; filename="papers.csv"'
#         return response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .fetcher import fetch_and_filter_papers
from .serializers import papers_to_csv

class PubMedFetchView(APIView):
    def get(self, request):
        query = request.query_params.get("query", None)
        is_export = request.query_params.get("is_export", "false").lower() == "true"  # Convert to boolean
        
        if not query:
            return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"🔍 Fetching papers for query: {query}")
        
        # Fetch and filter papers
        papers = fetch_and_filter_papers(query)
        
        print(f"✅ Papers fetched: {len(papers)}")  # Check how many papers were retrieved
        for i, paper in enumerate(papers[:3]):  # Print first 3 for debugging
            print(f"📄 Paper {i+1}: {paper}")

        if not papers:
            return Response({"detail": "No papers found."}, status=status.HTTP_404_NOT_FOUND)

        if is_export:
            print("📂 Exporting papers to CSV...")
            csv_data = papers_to_csv(papers)
            print(f"✅ CSV Data:\n{csv_data[:500]}")  # Print first 500 chars for verification

            # Prepare the response with correct CSV headers
            response = Response(csv_data, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="papers.csv"'
            return response
        else:
            print("📊 Returning JSON response...")
            return Response({"papers": papers}, status=status.HTTP_200_OK)
