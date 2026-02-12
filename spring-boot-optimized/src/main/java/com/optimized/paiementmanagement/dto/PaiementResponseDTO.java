package com.optimized.paiementmanagement.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Payment Response DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PaiementResponseDTO {
    
    private Long id;
    private Long reservationId;
    private BigDecimal montant;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime datePaiement;
    
    private String status;
    private String modePaiement;
    private String transactionId;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdDate;
}
