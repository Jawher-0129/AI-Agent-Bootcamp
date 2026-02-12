package com.optimized.paiementmanagement.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Payment Request DTO - Optimized with:
 * - Jakarta validation annotations
 * - Proper constraints
 * - Immutable design consideration
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PaiementRequestDTO {
    
    @NotNull(message = "Reservation ID is required")
    @Positive(message = "Reservation ID must be positive")
    private Long reservationId;
    
    @NotNull(message = "Amount is required")
    @DecimalMin(value = "0.01", message = "Amount must be greater than 0")
    @Digits(integer = 10, fraction = 2, message = "Invalid amount format")
    private BigDecimal montant;
    
    @NotBlank(message = "Payment mode is required")
    @Size(max = 50, message = "Payment mode must not exceed 50 characters")
    private String modePaiement;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime datePaiement;
}
